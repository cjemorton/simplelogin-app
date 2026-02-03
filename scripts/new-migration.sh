#!/usr/bin/env sh
# new-migration.sh - Generate a new database migration script using Docker
# To run it: sh scripts/new-migration.sh
# This creates a temporary PostgreSQL container, upgrades to latest schema,
# generates migration, then cleans up

container_name=sl-db-new-migration

# create a postgres database for SimpleLogin
docker rm -f ${container_name}
docker run -p 25432:5432 --name ${container_name} -e POSTGRES_PASSWORD=postgres -e POSTGRES_DB=sl -d postgres:16-alpine

# sleep a little bit for the db to be ready
sleep 3

# upgrade the DB to the latest stage and
env DB_URI=postgresql://postgres:postgres@127.0.0.1:25432/sl uv run alembic upgrade head

# generate the migration script.
env DB_URI=postgresql://postgres:postgres@127.0.0.1:25432/sl uv run alembic revision --autogenerate $@

# remove the db
docker rm -f ${container_name}
