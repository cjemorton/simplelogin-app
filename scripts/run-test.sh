#!/usr/bin/env sh
# run-test.sh - Run the test suite with a temporary PostgreSQL container
# This script creates a test database, runs migrations, executes tests, then cleans up

# Delete the test DB if it isn't properly removed
docker rm -f sl-test-db

# Create a test DB with latest PostgreSQL
docker run -d --name sl-test-db -e POSTGRES_PASSWORD=test -e POSTGRES_USER=test -e POSTGRES_DB=test -p 15432:5432 postgres:16-alpine

# the time for the test DB container to start
sleep 3

# migrate the DB to the latest version
CONFIG=tests/test.env uv run alembic upgrade head

# run test
uv run pytest -c pytest.ci.ini

# Delete the test DB
docker rm -f sl-test-db
