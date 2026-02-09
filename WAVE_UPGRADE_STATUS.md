# Wave Upgrade Status

This document tracks the phased modernization of the SimpleLogin application infrastructure and dependencies.

## Overview

The upgrade process is divided into three waves to minimize risk and ensure stability:

- **Wave 1**: Foundation and Security - Docker environment and critical security dependencies
- **Wave 2**: Flask Ecosystem - Flask, Werkzeug, and related web framework components  
- **Wave 3**: Data Layer - SQLAlchemy 2.0 migration and database-related upgrades

---

## Wave 1: Foundation and Security (COMPLETED)

**Status**: ✅ Complete  
**Branch**: `copilot/upgrade-dependencies-and-docker`

### Objectives

- Modernize Docker base images for better security and performance
- Upgrade critical security-related dependencies
- Update development tooling to latest stable versions
- Ensure compatibility with Python 3.12

### Changes Implemented

#### Docker Environment
- **Ubuntu**: 22.04 → 24.04 LTS
- **Node.js**: 10.17.0 → 22.x LTS (latest LTS version)

#### Security Dependencies
- **cryptography**: 37.0.1 → 44.0.3
  - Removed deprecated `backend` parameter from HKDF instantiation
  - Updated `app/abuser_utils.py` to remove `default_backend()` import and usage
  - Updated `tests/test_abuser_utils.py` to remove `default_backend()` import and usage
- **pyOpenSSL**: 19.1.0 → 25.1.0
- **requests**: 2.25.1 → 2.32.5
- **gunicorn**: 20.0.4 → 23.0.0

#### Development Dependencies
- **pytest**: 7.0.1 → 8.4.2
- **black**: 22.1.0 → 24.1.1
- **ruff**: 0.1.5 → 0.9.10
- **pylint**: 2.14.4 → 3.3.9

#### Code Changes
- Removed `from cryptography.hazmat.backends import default_backend` imports
- Removed `backend=default_backend()` parameters from HKDF instantiation calls
- Updated files:
  - `/app/abuser_utils.py`
  - `/tests/test_abuser_utils.py`

### Testing & Validation

- ✅ All tests pass
- ✅ Linting passes (pre-commit hooks, black, ruff, pylint)
- ✅ Security scan passes (CodeQL)
- ✅ Dependency vulnerability scan passes (GitHub Advisory Database)

### Migration Notes

**Breaking Changes**: None - all changes are backward compatible within the scope of this wave.

**API Compatibility**: The removal of the `backend` parameter from cryptography is required for cryptography >= 42.0.0. This change is transparent to the application logic.

---

## Wave 2: Flask Ecosystem (PLANNED)

**Status**: 🔲 Not Started  
**Target Branch**: TBD

### Objectives

- Upgrade Flask to 2.x or 3.x
- Upgrade Werkzeug to compatible version
- Update Flask extensions (Flask-Login, Flask-Migrate, Flask-Admin, etc.)
- Ensure compatibility with application routing and middleware

### Planned Changes

- **Flask**: 1.1.2 → 3.x (TBD based on compatibility testing)
- **Werkzeug**: 1.0.1 → 3.x (TBD)
- **Flask-Login**: 0.5.0 → 0.6.x
- **Flask-Migrate**: 2.5.3 → 4.x
- **Flask-Admin**: 1.5.6 → 1.6.x
- **Other Flask extensions**: To be determined

### Risks & Considerations

- Potential breaking changes in Flask 2.x/3.x routing
- Werkzeug API changes
- Jinja2 template compatibility
- Session management changes

---

## Wave 3: Data Layer (PLANNED)

**Status**: 🔲 Not Started  
**Target Branch**: TBD

### Objectives

- Migrate to SQLAlchemy 2.0
- Update database query patterns to use new API
- Modernize ORM patterns and relationships
- Ensure migration script compatibility

### Planned Changes

- **SQLAlchemy**: 1.3.24 → 2.0.x
- **sqlalchemy-utils**: 0.36.8 → 0.41.x
- **Alembic/Flask-Migrate**: Update to support SQLAlchemy 2.0

### Risks & Considerations

- Breaking changes in SQLAlchemy 2.0 query API
- Deprecated patterns (e.g., `Query.filter_by()` vs `select()`)
- ORM relationship definitions
- Migration script compatibility
- Database session management

---

## General Guidelines

### Testing Strategy

For each wave:
1. Run full test suite before changes
2. Make incremental changes
3. Run tests after each significant change
4. Run linters and formatters
5. Perform manual smoke testing of critical paths
6. Run security scans

### Rollback Plan

Each wave is implemented in a separate branch. If issues arise:
1. Fix-forward if possible (minor issues)
2. Revert the branch if major issues are discovered
3. Re-evaluate the upgrade strategy for the problematic components

### Documentation

- Update this file after completing each wave
- Document any breaking changes in commit messages
- Update README.md if deployment procedures change
- Update CONTRIBUTING.md if development setup changes

---

## Continuation Prompts

Use these prompts to continue with subsequent waves:

### Wave 2 Prompt
```
Continue with Wave 2 upgrades for the SimpleLogin application as documented in WAVE_UPGRADE_STATUS.md. 
Upgrade Flask and related web framework components while maintaining compatibility with the existing 
application structure. Follow the testing and validation procedures outlined in Wave 1.
```

### Wave 3 Prompt
```
Continue with Wave 3 upgrades for the SimpleLogin application as documented in WAVE_UPGRADE_STATUS.md.
Migrate to SQLAlchemy 2.0 and update database query patterns. Follow the testing and validation 
procedures outlined in previous waves.
```

---

## Contact & Support

For questions or issues related to these upgrades:
- Open an issue in the repository
- Reference this document and the specific wave
- Include test results and error logs if applicable
