#!/usr/bin/env sh
# reset_test_db.sh - Reset the test database
# WARNING: This will destroy all data in the test database!

export DB_URI=postgresql://myuser:mypassword@localhost:15432/test
echo 'drop schema public cascade; create schema public;' | psql  $DB_URI

uv run alembic upgrade head
