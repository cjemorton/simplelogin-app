import email
import json
import os
import random
import string
from datetime import date, timedelta
from email.message import EmailMessage
from typing import Optional, Dict

import jinja2
from flask import url_for

from app.db import Session
from app.models import User, PartnerUser, UserAliasDeleteAction
from app.proton.proton_partner import get_proton_partner
from app.utils import random_string

# Counter for generating unique dates in tests to avoid DB unique constraint violations
_date_counter = 0


def create_new_user(
    email: Optional[str] = None,
    name: Optional[str] = None,
    alias_delete_action: UserAliasDeleteAction = UserAliasDeleteAction.DeleteImmediately,
) -> User:
    if not email:
        email = f"user_{random_token(10)}@mailbox.lan"
    if not name:
        name = "Test User"
    # new user has a different email address
    user = User.create(
        email=email,
        password="password",
        name=name,
        activated=True,
        flush=True,
    )
    user.alias_delete_action = alias_delete_action
    Session.flush()

    return user


def create_partner_linked_user() -> tuple[User, PartnerUser]:
    user = create_new_user()
    partner_user = PartnerUser.create(
        partner_id=get_proton_partner().id,
        user_id=user.id,
        external_user_id=random_token(10),
        flush=True,
    )

    return user, partner_user


def login(flask_client, user: Optional[User] = None) -> User:
    if not user:
        user = create_new_user()

    r = flask_client.post(
        url_for("auth.login"),
        data={"email": user.email, "password": "password"},
        follow_redirects=True,
    )

    assert r.status_code == 200
    assert b"/auth/logout" in r.data

    return user


def random_domain() -> str:
    return random_token() + ".lan"


def random_token(length: int = 10) -> str:
    return "".join(random.choices(string.ascii_lowercase + string.digits, k=length))


def pretty(d):
    """pretty print as json"""
    print(json.dumps(d, indent=2))


def load_eml_file(
    filename: str, template_values: Optional[Dict[str, str]] = None
) -> EmailMessage:
    emails_dir = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "example_emls"
    )
    fullpath = os.path.join(emails_dir, filename)
    with open(fullpath) as fd:
        template = jinja2.Template(fd.read())
        if not template_values:
            template_values = {}
        rendered = template.render(**template_values)
        return email.message_from_bytes(rendered.encode("utf-8"))


def random_email() -> str:
    return "{rand}@{rand}.com".format(rand=random_string(20))


def fix_rate_limit_after_request():
    from flask import g
    from app.extensions import limiter

    g._rate_limiting_complete = False
    setattr(g, "%s_rate_limiting_complete" % limiter._key_prefix, False)


def get_unique_date() -> date:
    """
    Generate a unique date for test purposes.

    This function generates unique dates by combining a base date with an incrementing counter
    and a random offset. This ensures that tests running in parallel (e.g., with pytest-xdist)
    won't create database entries with duplicate dates, avoiding unique constraint violations
    on the daily_metric table.

    Returns:
        date: A unique date object safe to use in parallel test execution
    """
    global _date_counter
    _date_counter += 1
    # Use a base date far in the past (year 2000) to avoid conflicts with real data
    # Add counter + random offset to ensure uniqueness across parallel test runs
    base_date = date(2000, 1, 1)
    # Random offset up to 10000 days plus counter to ensure uniqueness
    offset_days = _date_counter + random.randint(0, 10000)
    return base_date + timedelta(days=offset_days)
