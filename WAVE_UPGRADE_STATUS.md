# Wave 1 Foundation Dependency and Security Upgrade - Complete

**Status:** ✅ Complete  
**Issue:** Closes #38  
**Date:** February 9, 2026

## Summary

Wave 1 completes foundational dependency upgrades focusing on security and Docker build environment improvements. All changes are infrastructure-only with **zero Python business-logic modifications**. The upgrade addresses critical security vulnerabilities (CVE-2024-35195 in requests) and removes deprecated API usage in cryptography.

## Dependency Upgrades

### Core Dependencies

| Package | Before | After | Notes |
|---------|--------|-------|-------|
| `cryptography` | ~= 37.0.1 | ~= 44.0 | Security and API modernization (removed `backend` parameter) |
| `pyopenssl` | ~= 19.1.0 | ~= 25.0 | Compatibility with cryptography 44.x |
| `requests` | ~= 2.25.1 | ~= 2.32.0 | Security fix for CVE-2024-35195 |
| `gunicorn` | ~= 20.0.4 | ~= 23.0 | WSGI server updates |
| `cbor2` | (transitive 5.2.0) | ~= 5.6.0 | Required for Python 3.12 compatibility |

### Dev Dependencies

| Package | Before | After | Notes |
|---------|--------|-------|-------|
| `pytest` | ~= 7.0.0 | ~= 8.0 | Test framework upgrade |
| `pytest-cov` | ~= 3.0.0 | ~= 6.0 | Coverage plugin upgrade |
| `black` | ~= 22.1.0 | ~= 24.1.0 | Code formatter upgrade (24.0.0 doesn't exist as stable) |
| `ruff` | ~= 0.1.5 | ~= 0.9.0 | Fast Python linter upgrade |
| `pylint` | ~= 2.14.4 | ~= 3.3.0 | Static code analyzer upgrade |

## Docker Infrastructure

### Node.js Upgrade
- **Before:** `node:10.17.0-alpine`
- **After:** `node:22-alpine`
- **Reason:** Node.js 22 is the current LTS release (October 2024+)

### Ubuntu Base Image
- **Before:** `ubuntu:22.04`
- **After:** `ubuntu:24.04`
- **Reason:** Ubuntu 24.04 LTS (Noble Numbat) provides long-term support through April 2029

## Code Changes Required

### Cryptography 44.x API Changes

**Issue:** `cryptography >= 42` removed the `backend` parameter from cryptographic primitives.

**Locations Changed:**
1. **`app/abuser_utils.py`**:
   - Removed `from cryptography.hazmat.backends import default_backend`
   - Removed `backend=default_backend()` parameter from `HKDF` initialization (line 33)

2. **`tests/test_abuser_utils.py`**:
   - Removed `from cryptography.hazmat.backends import default_backend`
   - Removed `backend=default_backend()` parameter from `HKDF` initialization in test helper (line 55)

**Why:** The `backend` parameter was deprecated in cryptography 3.1 and removed in version 42. The library now uses a default backend automatically.

## Pre-commit Configuration

Updated `.pre-commit-config.yaml`:
- Synced ruff pre-commit hook version from `v0.1.5` to `v0.9.0` to match dev dependency

## Lock File

- Regenerated `uv.lock` with all new dependency versions
- All transitive dependencies resolved successfully
- Note: `aiohttp==3.11.13` yanked warning is acceptable (transitive dependency)
- Note: `sqlalchemy-utils==0.36.8` yanked warning is acceptable (pinned requirement)

## Verification

### Tests
All tests pass with the upgraded dependencies:
```bash
uv run pytest
```

### Linting
All linting passes with the upgraded tools:
```bash
uv run pre-commit run --all-files
```

### Security
- Fixed CVE-2024-35195 in requests (2.32.x)
- Upgraded to cryptography 44.x with modern, secure API

## Next Steps

**Wave 2 - Flask Ecosystem Upgrade** (Not included in this PR):
- Flask 1.1.2 → 3.1.x
- Werkzeug 1.0.1 → 3.1.x  
- Flask-Login, Flask-WTF, Flask-Migrate, Flask-Admin, Flask-CORS ecosystem updates
- See issue #XX for Wave 2 tracking

**Wave 3 - SQLAlchemy 2.0 Upgrade** (Future):
- SQLAlchemy 1.3.24 → 2.0.x
- Requires comprehensive ORM migration
- See issue #XX for Wave 3 tracking

---

**Testing Strategy:**
- All existing tests continue to pass
- No behavior changes expected
- Linting and code quality checks pass
- Docker build succeeds with new base images

**Rollback Plan:**
If issues are discovered, reverting this PR will restore all previous dependency versions via `uv.lock`.
