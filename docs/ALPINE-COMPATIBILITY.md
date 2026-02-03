# Alpine Linux Compatibility Notes

## Current Status: Experimental

The Alpine-based Docker images (Dockerfile.production and Dockerfile.dev) are currently **experimental** due to dependencies that don't have pre-built wheels for Alpine's musl libc.

##  Known Issues

### 1. sl-pgp Dependency

The `sl-pgp` package provides pre-built wheels only for glibc-based systems (manylinux):
- ✅ Available: `manylinux_2_31_x86_64`, `manylinux_2_31_aarch64`
- ❌ Not available: `musllinux` (Alpine)

**Impact**: Cannot install sl-pgp from PyPI on Alpine without building from source.

**Workarounds**:
1. **Build from source** (requires Rust toolchain and build dependencies)
2. **Use glibc compatibility layer** (adds complexity)
3. **Request Alpine wheels** from sl-pgp maintainers
4. **Use Ubuntu-based image** (recommended for production)

### 2. Other Native Dependencies

Dependencies that may have limited Alpine support:
- `pyre2` - RE2 regular expression library bindings
- `psycopg2-binary` - PostgreSQL adapter
- Native extensions requiring specific glibc features

## Recommended Approach

### For Production

**Use the Ubuntu-based Dockerfile** until Alpine compatibility is fully resolved:

```bash
# This works out of the box
docker build -f Dockerfile -t simplelogin/app:latest .
```

The Ubuntu-based image:
- ✅ All dependencies work without modifications
- ✅ Well-tested and production-ready
- ✅ Pre-built wheels available
- ⚠️ Larger image size (~1.2GB vs ~450MB Alpine)

### For Development

Either Ubuntu or Alpine can work, depending on your needs:

```bash
# Ubuntu-based dev environment (recommended)
docker build -f Dockerfile -t simplelogin/app:dev .

# Alpine-based dev environment (experimental)
docker build -f Dockerfile.dev -t simplelogin/app:dev-alpine .
```

## Future Work

To make Alpine fully production-ready, we need to:

1. **Build sl-pgp for Alpine**
   - Create Alpine-specific wheel builds
   - Publish to PyPI or host separately
   - Or vendor the wheel in the repository

2. **Test all native dependencies on Alpine**
   - Verify pyre2, psycopg2, and other native modules
   - Document any additional build requirements
   - Create Alpine-specific build scripts if needed

3. **Upstream fixes**
   - Submit PRs to dependency maintainers for Alpine support
   - Create Alpine packages for key dependencies

## Building sl-pgp from Source (Advanced)

If you want to use Alpine and build sl-pgp from source:

```dockerfile
# Add to Dockerfile.production before uv sync
RUN apk add --no-cache rust cargo && \
    cd /tmp && \
    git clone https://github.com/simple-login/sl-pgp-rs.git && \
    cd sl-pgp-rs && \
    # Build and install sl-pgp
    cargo build --release && \
    # Install into venv...
    # (specific steps depend on sl-pgp build process)
```

**Note**: This significantly increases build time and image size.

## Why Alpine?

Despite current limitations, Alpine offers advantages:

- **Smaller base image**: 5MB vs 77MB (Ubuntu)
- **Security**: Minimal attack surface
- **Speed**: Faster downloads and container startup
- **Resource efficiency**: Lower memory footprint

## Monitoring Progress

Track Alpine compatibility progress in:
- [Issue #XXXX](https://github.com/simple-login/app/issues/XXXX) - Alpine Docker Support
- [sl-pgp-rs Repository](https://github.com/simple-login/sl-pgp-rs) - Watch for Alpine wheel releases

## Feedback

If you're using or want to use Alpine-based images, please:
1. Comment on the tracking issue with your use case
2. Help test and report compatibility issues
3. Contribute Alpine-specific fixes or workarounds

## See Also

- [Migration Guide](./MIGRATION-ALPINE.md) - Full migration documentation
- [Build Documentation](./build-image.md) - Building images
- [Dockerfile](../Dockerfile) - Current production Ubuntu-based Dockerfile
