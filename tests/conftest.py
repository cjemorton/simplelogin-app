import os

from flask import testing

# use the tests/test.env config fle
# flake8: noqa: E402

os.environ["CONFIG"] = os.path.abspath(
    os.path.join(os.path.dirname(os.path.dirname(__file__)), "tests/test.env")
)
import sqlalchemy

from app.db import Session, engine, connection
from app.rate_limiter import set_rate_limit_enabled

import pytest

from server import create_app
from init_app import add_sl_domains, add_proton_partner

# Disable rate limit for tests
set_rate_limit_enabled(False)

app = create_app()
app.config["TESTING"] = True
app.config["WTF_CSRF_ENABLED"] = False
app.config["SERVER_NAME"] = "sl.lan"

# enable pg_trgm extension (idempotent, safe under parallel execution)
with engine.connect() as conn:
    try:
        conn.execute(sqlalchemy.text("CREATE EXTENSION IF NOT EXISTS pg_trgm"))
    except sqlalchemy.exc.SQLAlchemyError as e:
        import warnings
        warnings.warn(f"Could not create pg_trgm extension: {e}")

add_sl_domains()
add_proton_partner()


@pytest.fixture(scope="session", autouse=True)
def clear_daily_metric_table():
    """Clear daily_metric table to prevent duplicate key violations in parallel tests.

    When running with pytest-xdist, multiple workers may call
    DailyMetric.get_or_create_today_metric() concurrently, causing
    UniqueViolation on the daily_metric_date_key constraint.
    """
    try:
        with engine.begin() as conn:
            conn.execute(sqlalchemy.text("DELETE FROM daily_metric"))
    except sqlalchemy.exc.SQLAlchemyError as e:
        import warnings
        warnings.warn(f"Could not clear daily_metric table: {e}")


@pytest.fixture
def flask_app():
    yield app


from app import config, constants


class CustomTestClient(testing.FlaskClient):
    def open(self, *args, **kwargs):
        if isinstance(args[0], str):
            headers = kwargs.pop("headers", {})
            headers.update({constants.HEADER_ALLOW_API_COOKIES: "allow"})
            kwargs["headers"] = headers
        return super().open(*args, **kwargs)


@pytest.fixture
def flask_client():
    transaction = connection.begin()

    with app.app_context():
        # disable rate limit during test
        config.DISABLE_RATE_LIMIT = True
        try:
            app.test_client_class = CustomTestClient
            client = app.test_client()
            client.environ_base[constants.HEADER_ALLOW_API_COOKIES] = "allow"
            yield client
        finally:
            # disable rate limit again as some tests might enable rate limit
            config.DISABLE_RATE_LIMIT = True
            # roll back all commits made during a test
            transaction.rollback()
            Session.rollback()
            Session.close()
