# Migration Guide: Alpine-based Architecture

This guide helps existing SimpleLogin deployments migrate to the new Alpine-based Docker architecture.

## Overview of Changes

The refactor introduces several improvements:

1. **Alpine Linux Base**: Smaller, more secure container images
2. **Multi-stage Builds**: Separate build and runtime dependencies for optimal image size
3. **Dev/Production Split**: Dedicated Dockerfiles for development and production
4. **Improved Security**: Non-root user, health checks, minimal attack surface
5. **Better Performance**: Optimized layer caching, reduced image size
6. **Updated Dependencies**: PostgreSQL 16, Node 20, Python 3.12

## Image Size Comparison

- **Old Ubuntu-based image**: ~1.2GB
- **New Alpine production image**: ~400-500MB (60-70% reduction)
- **New Alpine dev image**: ~600-700MB (includes dev tools)

## Breaking Changes

### 1. Dockerfile Names

**Before:**
```bash
docker build -t simplelogin/app .
```

**After (Production):**
```bash
docker build -f Dockerfile.production -t simplelogin/app:production .
```

**After (Development):**
```bash
docker build -f Dockerfile.dev -t simplelogin/app:dev .
```

### 2. Base Image

- **Old**: `ubuntu:22.04`
- **New**: `python:3.12-alpine`

### 3. Package Manager

- **Old**: `apt-get`
- **New**: `apk`

### 4. User Context

The new images run as a non-root user (`simplelogin:simplelogin` with UID/GID 1000).

**Impact**: If you mount volumes, ensure proper permissions:
```bash
sudo chown -R 1000:1000 /path/to/volumes
```

### 5. PostgreSQL Version

- **Old**: PostgreSQL 13
- **New**: PostgreSQL 16 (Alpine-based)

**Migration**: See PostgreSQL upgrade guide below.

## Migration Steps

### Step 1: Backup Your Data

**Critical**: Always backup before upgrading!

```bash
# Backup database
docker exec simplelogin-db pg_dump -U postgres simplelogin > backup-$(date +%Y%m%d).sql

# Backup volumes
docker run --rm -v simplelogin_data:/data -v $(pwd):/backup alpine tar czf /backup/volumes-$(date +%Y%m%d).tar.gz /data
```

### Step 2: Update PostgreSQL (if needed)

If you're running PostgreSQL 13 or older:

```bash
# Stop current containers
docker-compose down

# Update docker-compose.yml to use postgres:16-alpine
# Then start with new version
docker-compose up -d postgres

# The database will automatically upgrade
```

**Note**: PostgreSQL 16 is backward compatible with PostgreSQL 13 data directories, but verify in your environment.

### Step 3: Pull New Images

```bash
# Pull the new Alpine-based image
docker pull simplelogin/app-ci:latest

# Or build locally
docker build -f Dockerfile.production -t simplelogin/app:production .
```

### Step 4: Update docker-compose.yml

Update your `docker-compose.yml`:

```yaml
version: '3.8'

services:
  db:
    image: postgres:16-alpine
    # ... rest of config

  app:
    image: simplelogin/app-ci:latest
    # Or build from local Dockerfile
    # build:
    #   context: .
    #   dockerfile: Dockerfile.production
    volumes:
      # Ensure volume permissions are correct for UID 1000
      - ./data:/code/local_data
    # ... rest of config
```

### Step 5: Fix Volume Permissions

```bash
# Adjust ownership for non-root user
sudo chown -R 1000:1000 ./data
sudo chown -R 1000:1000 ./static/upload
```

### Step 6: Deploy

```bash
# Start with new images
docker-compose up -d

# Check logs
docker-compose logs -f app

# Verify health
curl http://localhost:7777/health
```

## Development Environment

### Using Dockerfile.dev

The development Dockerfile includes:
- All build tools (gcc, g++, cmake, etc.)
- Development dependencies (pytest, black, pylint, etc.)
- Live reload support
- Debugging tools

**docker-compose.dev.yml example:**

```yaml
version: '3.8'

services:
  app:
    build:
      context: .
      dockerfile: Dockerfile.dev
    volumes:
      - .:/code
      - /code/.venv  # Prevent overwriting venv
    ports:
      - "7777:7777"
      - "5678:5678"  # Debugger port
    environment:
      - FLASK_ENV=development
      - FLASK_DEBUG=1
    command: flask run --host=0.0.0.0 --port=7777 --reload --debug
```

### Live Development

```bash
# Start dev environment
docker-compose -f docker-compose.dev.yml up

# Code changes will automatically reload
# Edit files locally, see changes immediately
```

## Troubleshooting

### Issue: Permission Denied Errors

**Symptom**: Application can't write to mounted volumes

**Solution**:
```bash
sudo chown -R 1000:1000 /path/to/volumes
```

### Issue: Native Module Compilation Fails

**Symptom**: Errors building pyre2, psycopg2-binary, etc.

**Solution**: The Dockerfile.production includes all necessary build dependencies. If building locally, ensure you have:
- `alpine-sdk` (or build-essential)
- `postgresql-dev`
- `re2-dev`

### Issue: Database Connection Fails

**Symptom**: Can't connect to PostgreSQL

**Solution**:
1. Verify PostgreSQL is running: `docker-compose ps`
2. Check connection string in `.env`
3. Ensure database is ready: `docker-compose logs db`

### Issue: Image Build Fails on ARM/Apple Silicon

**Symptom**: Build errors on M1/M2 Macs

**Solution**: Use buildx for multi-platform:
```bash
docker buildx build --platform linux/amd64,linux/arm64 -f Dockerfile.production -t simplelogin/app:production .
```

## Rollback Procedure

If you encounter issues:

```bash
# Stop new containers
docker-compose down

# Restore from backup
cat backup-YYYYMMDD.sql | docker exec -i simplelogin-db psql -U postgres simplelogin

# Use old image
docker-compose -f docker-compose.old.yml up -d
```

## Additional Resources

- [Alpine Linux Package Search](https://pkgs.alpinelinux.org/packages)
- [Docker Multi-stage Builds](https://docs.docker.com/build/building/multi-stage/)
- [PostgreSQL 16 Release Notes](https://www.postgresql.org/docs/16/release-16.html)

## Getting Help

- GitHub Issues: https://github.com/simple-login/app/issues
- Forum: https://github.com/simple-login/app/discussions
- Documentation: [/docs](/docs)

## Changelog

See [CHANGELOG.md](./CHANGELOG.md) for detailed version history.
