import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker

from app import config


engine = create_engine(
    config.DB_URI, connect_args={"application_name": config.DB_CONN_NAME}
)

# SQLAlchemy 2.0: Bind session to engine instead of connection
# This is the recommended pattern for 2.0
Session = scoped_session(sessionmaker(bind=engine))

# Module-level connection for backward compatibility with tests
# TODO: This connection is created on import and never explicitly closed.
# Future improvement: Migrate tests to use context-managed connections
# (e.g., `with engine.connect() as conn:`) and remove this global.
# For now, keeping for compatibility with tests/conftest.py
connection = engine.connect()

# Session is actually a proxy, more info on
# https://docs.sqlalchemy.org/en/14/orm/contextual.html?highlight=scoped_session#implicit-method-access
Session: sqlalchemy.orm.Session
