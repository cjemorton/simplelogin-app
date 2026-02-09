# Run tests
# This script runs tests locally using Docker for the test database.
# For parallel testing similar to CI, install pytest-xdist and pytest-shard:
#   uv pip install pytest-xdist pytest-shard
# Then run with sharding:
#   uv run pytest -c pytest.ci.ini --shard-id=1 --num-shards=4 -n auto
# where --shard-id splits tests into 4 groups, and -n auto uses all CPU cores

# Delete the test DB if it isn't properly removed
docker rm -f sl-test-db

# Create a test DB
docker run -d --name sl-test-db -e POSTGRES_PASSWORD=test -e POSTGRES_USER=test -e POSTGRES_DB=test -p 15432:5432 postgres:13

# the time for the test DB container to start
sleep 3

# migrate the DB to the latest version
CONFIG=tests/test.env uv run alembic upgrade head

# run test
uv run pytest -c pytest.ci.ini

# Delete the test DB
docker rm -f sl-test-db
