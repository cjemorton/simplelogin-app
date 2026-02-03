from flask import url_for

from app import config
from app.db import Session
from app.models import DailyMetric, User
from app.utils import canonicalize_email
from tests.utils import create_new_user, random_email, get_unique_date


def setup_module():
    config.SKIP_MX_LOOKUP_ON_CHECK = True


def teardown_module():
    config.SKIP_MX_LOOKUP_ON_CHECK = False


def test_register_success(flask_client):
    email = random_email()
    r = flask_client.post(
        url_for("auth.register"),
        data={"email": email, "password": "password"},
        follow_redirects=True,
    )

    assert r.status_code == 200
    # User arrives at the waiting activation page.
    assert b"An email to validate your email is on its way" in r.data


def test_register_increment_nb_new_web_non_proton_user(flask_client, monkeypatch):
    """Test that registration increments the daily metric counter.

    This test uses a unique date to avoid unique constraint violations when tests
    run in parallel (e.g., with pytest-xdist across multiple shards).
    """
    # Generate a unique test date to avoid conflicts with other parallel tests
    test_date = get_unique_date()

    # Mock arrow.utcnow() to return our test date
    class MockArrow:
        @staticmethod
        def date():
            return test_date

    def mock_utcnow():
        return MockArrow()

    # Patch arrow.utcnow in the models module where get_or_create_today_metric is defined
    monkeypatch.setattr("app.models.arrow.utcnow", mock_utcnow)

    # Create the daily metric for our test date
    daily_metric = DailyMetric.create(
        date=test_date, nb_new_web_non_proton_user=0, nb_alias=0
    )
    Session.commit()
    nb_new_web_non_proton_user = daily_metric.nb_new_web_non_proton_user

    r = flask_client.post(
        url_for("auth.register"),
        data={"email": random_email(), "password": "password"},
        follow_redirects=True,
    )

    assert r.status_code == 200
    # Verify the metric was incremented
    Session.refresh(daily_metric)
    assert daily_metric.nb_new_web_non_proton_user == nb_new_web_non_proton_user + 1


def test_register_disabled(flask_client):
    """User cannot create new account when DISABLE_REGISTRATION."""

    config.DISABLE_REGISTRATION = True

    r = flask_client.post(
        url_for("auth.register"),
        data={"email": "abcd@gmail.com", "password": "password"},
        follow_redirects=True,
    )

    config.DISABLE_REGISTRATION = False
    assert b"Registration is closed" in r.data


def test_register_non_canonical_if_canonical_exists_is_not_allowed(flask_client):
    """User cannot create new account if the canonical name clashes"""
    email = f"noncan.{random_email()}"
    canonical_email = canonicalize_email(email)
    create_new_user(email=canonical_email)

    r = flask_client.post(
        url_for("auth.register"),
        data={"email": email, "password": "password"},
        follow_redirects=True,
    )

    assert f"Email {canonical_email} already used".encode("utf-8") in r.data


def test_register_non_canonical_is_canonicalized(flask_client):
    """User cannot create new account if the canonical name clashes"""
    email = f"noncan.{random_email()}"

    r = flask_client.post(
        url_for("auth.register"),
        data={"email": email, "password": "password"},
        follow_redirects=True,
    )

    assert b"An email to validate your email is on its way" in r.data
    assert User.get_by(email=canonicalize_email(email)) is not None
