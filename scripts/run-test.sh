# Run tests locally or in CI
# 
# PREREQUISITES:
# Make sure pytest-xdist and pytest-shard are installed for parallelization:
#   uv pip install pytest-xdist pytest-shard
#
# LOCAL DEVELOPMENT:
# For faster local testing, use pytest-xdist to run tests in parallel:
#   uv run pytest -n auto
# 
# For testing a specific shard (useful for debugging CI failures):
#   uv run pytest --shard-id=1 --num-shards=4 -n auto
#
# CI ENVIRONMENT:
# In CI, tests are automatically split into 4 shards via GitHub Actions matrix
# Each shard runs: pytest -c pytest.ci.ini --shard-id=X --num-shards=4 -n auto
# - pytest-shard distributes tests across shards (--shard-id, --num-shards)
# - pytest-xdist parallelizes within each shard (-n auto uses all CPU cores)

# Delete the test DB if it isn't properly removed
docker rm -f sl-test-db

# Create a test DB
docker run -d --name sl-test-db -e POSTGRES_PASSWORD=test -e POSTGRES_USER=test -e POSTGRES_DB=test -p 15432:5432 postgres:13

# the time for the test DB container to start
sleep 3

# migrate the DB to the latest version
CONFIG=tests/test.env uv run alembic upgrade head

# run test
# For local testing with parallelization, you can use:
#   uv run pytest -c pytest.ci.ini -n auto
# For testing specific shards locally:
#   uv run pytest -c pytest.ci.ini --shard-id=1 --num-shards=4 -n auto
uv run pytest -c pytest.ci.ini

# Delete the test DB
docker rm -f sl-test-db
