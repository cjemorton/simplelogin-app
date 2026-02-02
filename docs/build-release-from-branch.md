# Building a Release from fix-pg_isready Branch

This document explains how to create a release build from the `fix-pg_isready` branch for testing purposes.

## Current Situation

The `fix-pg_isready` branch contains changes that add database readiness checks with `pg_isready` and psycopg2 fallback. This is a separate branch created for testing these improvements before merging to master.

The current GitHub Actions workflow (`.github/workflows/main.yml`) automatically builds and publishes Docker images **only** when:
- Pushing to the `master` branch, OR
- Pushing a tag starting with `v*` (e.g., `v1.2.3`)

## Options for Building a Release

### Option 1: Create a Test Tag (Recommended for Quick Testing)

This is the simplest approach - create a version tag on the `fix-pg_isready` branch to trigger the automated build pipeline.

**Steps:**

1. Checkout the fix-pg_isready branch:
   ```bash
   git checkout fix-pg_isready
   ```

2. Create and push a test tag:
   ```bash
   git tag v4.0.0-test-pg-isready
   git push origin v4.0.0-test-pg-isready
   ```

3. The GitHub Actions workflow will automatically:
   - Run tests and linting
   - Build the Docker image
   - Push it to Docker Hub as `simplelogin/app-ci:v4.0.0-test-pg-isready`
   - Create a GitHub release with changelog

4. Use the built image:
   ```bash
   docker pull simplelogin/app-ci:v4.0.0-test-pg-isready
   ```

**Cleanup after testing:**
```bash
# Delete the tag locally and remotely when done
git tag -d v4.0.0-test-pg-isready
git push --delete origin v4.0.0-test-pg-isready
```

### Option 2: Modify Workflow to Build from fix-pg_isready Branch

If you need continuous builds from this branch, modify the workflow to include it.

Add the `fix-pg_isready` branch to the build triggers in `.github/workflows/main.yml`:

```yaml
jobs:
  build:
    runs-on: ubuntu-latest
    needs: ['test', 'lint']
    # Change this line:
    if: github.event_name == 'push' && (github.ref == 'refs/heads/master' || github.ref == 'refs/heads/fix-pg_isready' || startsWith(github.ref, 'refs/tags/v'))
```

Then push to the branch to trigger a build.

### Option 3: Manual Docker Build (No CI/CD Required)

If you don't want to use GitHub Actions or don't have access to the CI/CD secrets:

1. Checkout the fix-pg_isready branch:
   ```bash
   git checkout fix-pg_isready
   ```

2. Build the Docker image locally:
   ```bash
   docker build -t simplelogin/app:test-pg-isready .
   ```

3. (Optional) Push to your own Docker registry:
   ```bash
   # Tag for your registry
   docker tag simplelogin/app:test-pg-isready your-registry.com/simplelogin/app:test-pg-isready
   
   # Login to your registry
   docker login your-registry.com
   
   # Push
   docker push your-registry.com/simplelogin/app:test-pg-isready
   ```

4. Use the locally built image in your deployment by updating your docker-compose or deployment scripts to use `simplelogin/app:test-pg-isready`.

## Recommended Approach

**For testing purposes**, we recommend **Option 1** (creating a test tag) because:
- ✅ It's the quickest and simplest
- ✅ Uses the existing CI/CD pipeline with all quality checks
- ✅ Produces a properly tested and tagged Docker image
- ✅ Can be easily cleaned up after testing
- ✅ Automatically creates a GitHub release for reference

## Using the Built Image

Once you have a built image (from any option above), update your deployment to use it:

1. Update your `simplelogin.env` or docker-compose file to reference the new image tag

2. In the deployment commands from the README, replace `simplelogin/app:3.4.0` with your new tag, for example:
   ```bash
   docker run -d \
       --name sl-app \
       -v $(pwd)/sl:/sl \
       -v $(pwd)/sl/upload:/code/static/upload \
       -v $(pwd)/simplelogin.env:/code/.env \
       -v $(pwd)/dkim.key:/dkim.key \
       -v $(pwd)/dkim.pub.key:/dkim.pub.key \
       -p 127.0.0.1:7777:7777 \
       --restart always \
       --network="sl-network" \
       simplelogin/app-ci:v4.0.0-test-pg-isready
   ```

## What's in the fix-pg_isready Branch?

The branch includes a new script `scripts/wait-for-db.sh` that:
- Uses `pg_isready` command if available (preferred method)
- Falls back to Python/psycopg2 if `pg_isready` is not found
- Properly handles database connection strings
- Includes security validations for extracted values
- Provides better logging and error messages

This ensures the SimpleLogin containers wait for PostgreSQL to be ready before starting, preventing startup errors.
