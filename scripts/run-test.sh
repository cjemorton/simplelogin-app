# Run tests
# This script sets up and runs the test suite locally

# Delete the test DB if it isn't properly removed
docker rm -f sl-test-db

# Create a test DB
docker run -d --name sl-test-db -e POSTGRES_PASSWORD=test -e POSTGRES_USER=test -e POSTGRES_DB=test -p 15432:5432 postgres:13

# the time for the test DB container to start
sleep 3

# migrate the DB to the latest version
CONFIG=tests/test.env uv run alembic upgrade head

# Run tests with CI configuration
# For parallel testing, add pytest-xdist and pytest-shard:
#   uv pip install pytest-xdist pytest-shard
# Then run with sharding and parallel execution:
#   uv run pytest -c pytest.ci.ini --shard-id=1 --num-shards=4 -n auto
# Or run all shards locally (requires multiple terminals or a script)
uv run pytest -c pytest.ci.ini

# Delete the test DB
docker rm -f sl-test-db
