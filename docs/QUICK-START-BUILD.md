# Quick Start: Building a Release from fix-pg_isready Branch

Need to build a Docker image from the `fix-pg_isready` branch for testing? This guide shows you the fastest way.

For detailed information and alternative methods, see [docs/build-release-from-branch.md](docs/build-release-from-branch.md).

## Fastest Method: Create a Test Tag

This will automatically trigger a build via GitHub Actions.

```bash
# 1. Checkout the fix-pg_isready branch
git checkout fix-pg_isready

# 2. Create and push a test tag
git tag v4.0.0-test-pg-isready
git push origin v4.0.0-test-pg-isready

# 3. Wait for GitHub Actions to complete (check Actions tab in GitHub)

# 4. Pull and use the built image
docker pull simplelogin/app-ci:v4.0.0-test-pg-isready
```

## Alternative: Manual Trigger via GitHub Actions UI

1. Go to your repository on GitHub
2. Click on "Actions" tab
3. Select "Build Test Release" workflow from the left sidebar
4. Click "Run workflow" button
5. Select the `fix-pg_isready` branch
6. Enter a tag suffix (e.g., `test-pg-isready`)
7. Click "Run workflow"

The image will be built and pushed as `simplelogin/app-ci:fix-pg_isready-test-pg-isready`

## Using the Built Image

Replace `simplelogin/app:3.4.0` with your new tag in all deployment commands. For example:

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

## Cleanup After Testing

```bash
# Delete the tag when you're done testing
git tag -d v4.0.0-test-pg-isready
git push --delete origin v4.0.0-test-pg-isready
```

## Need Help?

See the full documentation: [docs/build-release-from-branch.md](docs/build-release-from-branch.md)
