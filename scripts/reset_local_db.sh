#!/usr/bin/env sh
# reset_local_db.sh - Reset the local development database
# WARNING: This will destroy all data in the local database!

export DB_URI=postgresql://myuser:mypassword@localhost:15432/simplelogin
echo 'drop schema public cascade; create schema public;' | psql $DB_URI

uv run alembic upgrade head
uv run flask dummy-data
