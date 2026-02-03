# Building Docker Images

This guide explains how to build SimpleLogin Docker images for different platforms and purposes.

## Overview

SimpleLogin now uses Alpine Linux-based Docker images with separate configurations for development and production:

- **Dockerfile.production**: Optimized for production (minimal size, no dev tools)
- **Dockerfile.dev**: Includes development tools, debuggers, and live reload support
- **Dockerfile**: Legacy Ubuntu-based image (deprecated)

## Quick Start

### Production Build

```bash
# Single platform (local architecture)
docker build -f Dockerfile.production -t simplelogin/app:latest .

# Multi-platform (amd64 + arm64)
docker buildx build --platform linux/amd64,linux/arm64 \
  -f Dockerfile.production \
  -t simplelogin/app:latest .
```

### Development Build

```bash
docker build -f Dockerfile.dev -t simplelogin/app:dev .
```

## Multi-Architecture Builds

To build images that work on both x86_64 and ARM64 (Apple Silicon, AWS Graviton, etc.), use buildx.

### First Time Setup

Create a new buildx builder (only needed once):

```bash
docker buildx create --name simplelogin-builder --use
docker buildx inspect --bootstrap
```

### Build and Push Multi-arch Image

Replace `simplelogin/app:tag` with your desired image name and tag:

```bash
docker buildx build \
  --platform linux/amd64,linux/arm64 \
  --file Dockerfile.production \
  --tag simplelogin/app:v4.0.0 \
  --tag simplelogin/app:latest \
  --push \
  .
```

### Build Without Pushing (Load Locally)

**Note**: You can only load one platform at a time:

```bash
# For your local architecture
docker buildx build \
  --platform linux/amd64 \
  --file Dockerfile.production \
  --tag simplelogin/app:latest \
  --load \
  .
```

## Build Arguments

Both Dockerfiles support build arguments:

```bash
docker build \
  --file Dockerfile.production \
  --build-arg UV_VERSION=0.8.18 \
  --tag simplelogin/app:latest \
  .
```

Available build arguments:
- `UV_VERSION`: Version of uv package manager (default: 0.8.18)

## Image Tagging Strategy

### Production Images

Use semantic versioning:

```bash
# Major.minor.patch
docker tag simplelogin/app:latest simplelogin/app:4.0.0

# Major.minor (moving tag)
docker tag simplelogin/app:latest simplelogin/app:4.0

# Major (moving tag)
docker tag simplelogin/app:latest simplelogin/app:4

# Git SHA (for CI/CD)
docker tag simplelogin/app:latest simplelogin/app:sha-abc123f

# Latest (default)
docker tag simplelogin/app:latest simplelogin/app:latest
```

### Development Images

```bash
docker tag simplelogin/app:dev simplelogin/app:dev-latest
docker tag simplelogin/app:dev simplelogin/app:dev-feature-branch
```

## Optimization Tips

### Layer Caching

Docker caches layers for faster rebuilds. Order matters:

1. Copy dependency files first (package.json, pyproject.toml, uv.lock)
2. Install dependencies
3. Copy application code last

This is already optimized in both Dockerfiles.

### BuildKit Cache

Enable BuildKit for advanced caching:

```bash
export DOCKER_BUILDKIT=1

docker build \
  --file Dockerfile.production \
  --cache-from type=local,src=/tmp/cache \
  --cache-to type=local,dest=/tmp/cache \
  -t simplelogin/app:latest \
  .
```

### GitHub Actions Cache

In CI/CD (already configured in `.github/workflows/main.yml`):

```yaml
- name: Build and push
  uses: docker/build-push-action@v3
  with:
    cache-from: type=gha
    cache-to: type=gha,mode=max
```

## Image Size Comparison

| Image Type | Size | Use Case |
|------------|------|----------|
| Production (Alpine) | ~450MB | Production deployments |
| Development (Alpine) | ~650MB | Local development |
| Legacy (Ubuntu) | ~1.2GB | Deprecated |

## Building for Specific Platforms

### For Linux x86_64 (most servers)

```bash
docker buildx build \
  --platform linux/amd64 \
  -f Dockerfile.production \
  -t simplelogin/app:latest \
  .
```

### For ARM64 (Apple Silicon, AWS Graviton)

```bash
docker buildx build \
  --platform linux/arm64 \
  -f Dockerfile.production \
  -t simplelogin/app:latest \
  .
```

## Troubleshooting

### Issue: "No such file: python"

**Solution**: Make sure .python-version file exists and contains valid version.

### Issue: Native extension build fails

**Solution**: Dockerfile.production includes all necessary build dependencies. Verify the base image is correct.

### Issue: "Cannot find uv"

**Solution**: Check UV_VERSION build arg and network connectivity during build.

### Issue: Multi-arch build very slow

**Solution**: 
1. Use GitHub Actions or dedicated build servers
2. Enable BuildKit cache
3. Use qemu-user-static for cross-compilation

## CI/CD Integration

See `.github/workflows/main.yml` for production CI/CD example.

### Key Features:
- Multi-platform builds (amd64 + arm64)
- Layer caching via GitHub Actions cache
- Semantic versioning from Git tags
- Automated testing before build
- Metadata labels (version, SHA, timestamp)

## Local Development Workflow

```bash
# Build dev image
docker build -f Dockerfile.dev -t simplelogin-dev .

# Run with volume mount for live reload
docker run -it --rm \
  -v $(pwd):/code \
  -v /code/.venv \
  -p 7777:7777 \
  -e FLASK_ENV=development \
  simplelogin-dev

# Or use docker-compose
docker-compose -f docker-compose.dev.yml up
```

## Production Deployment

```bash
# Pull pre-built image
docker pull simplelogin/app-ci:latest

# Or build and run locally
docker build -f Dockerfile.production -t simplelogin/app:latest .
docker run -d -p 7777:7777 simplelogin/app:latest
```

## Security Scanning

Scan images for vulnerabilities:

```bash
# Using trivy
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock \
  aquasec/trivy image simplelogin/app:latest

# Using docker scout (requires Docker subscription)
docker scout cves simplelogin/app:latest
```

## Additional Resources

- [Docker Buildx Documentation](https://docs.docker.com/buildx/working-with-buildx/)
- [Multi-stage Builds Best Practices](https://docs.docker.com/develop/develop-images/multistage-build/)
- [Alpine Linux](https://alpinelinux.org/)

## See Also

- [Migration Guide](./MIGRATION-ALPINE.md) - Migrating from Ubuntu to Alpine
- [Quick Start Build](./QUICK-START-BUILD.md) - Getting started quickly
- [Build Release from Branch](./build-release-from-branch.md) - Release process