# SimpleLogin App — Modernization Wave Upgrade Status

**Last Updated:** 2026-02-09
**Tracking Issues:** #38 (Wave 1), #40 (Wave 2), #39 (Wave 3)

---

## Overview

This document tracks the phased modernization of the SimpleLogin application from its current
state (Flask 1.x, SQLAlchemy 1.3, numerous EOL dependencies) to a fully modern Python stack.

The upgrade is divided into 3 waves, executed sequentially to minimize risk:

| Wave | Scope | Status | Issue | PR |
|------|-------|--------|-------|-----|
| 1 | Foundation: Docker, cryptography, pyopenssl, gunicorn, dev tools | 🟡 In Progress | #38 | This PR |
| 2 | Flask Ecosystem: Flask 3.x, Werkzeug 3.x, all Flask extensions | ⬜ Not Started | #40 | — |
| 3 | SQLAlchemy 2.0+ Migration, Alembic, model refactors | ⬜ Not Started | #39 | — |

---

## Wave 1 — Foundation Dependency & Security Upgrade

### Changes Made

| Package | Before | After | Risk | Notes |
|---------|--------|-------|------|-------|
| `cryptography` | ~= 37.0.1 | ~= 44.0.0 | Medium | Security-critical. 7 major versions behind. API mostly stable. |
| `pyopenssl` | ~= 19.1.0 | ~= 25.0.0 | Medium | Coupled to cryptography upgrade |
| `requests` | ~= 2.25.1 | ~= 2.32.0 | Low | Backward compatible, security patches |
| `gunicorn` | ~= 20.0.4 | ~= 23.0.0 | Low | WSGI server, minimal config changes |
| `pytest` (dev) | ~= 7.0.0 | ~= 8.0.0 | Low | Dev-only |
| `black` (dev) | ~= 22.1.0 | ~= 24.0.0 | Low | Dev-only formatter |
| `ruff` (dev) | ~= 0.1.5 | ~= 0.9.0 | Low | Dev-only linter |
| `pylint` (dev) | ~= 2.14.4 | ~= 3.0.0 | Low | Dev-only linter |
| Node.js (Dockerfile) | 10.17.0 | 22-alpine (LTS) | Low | Only builds static assets |
| Ubuntu (Dockerfile) | 22.04 | 24.04 | Low | Base image update |

### What Was NOT Changed (Intentionally)

- **Flask** (1.1.2) — Requires coordinated Wave 2 migration
- **Werkzeug** (1.0.1) — Tightly coupled to Flask version
- **SQLAlchemy** (1.3.24) — Requires Wave 3 migration
- **itsdangerous** (1.1.0) — Coupled to Flask version
- **MarkupSafe** (1.1.1) — Coupled to Flask/Jinja2 version
- **Any application logic** — Zero code changes to `app/`, `server.py`, `email_handler.py`, etc.

---

## Wave 2 — Flask Ecosystem Modernization (Not Started)

### Planned Changes

When starting Wave 2, use the following prompt with GitHub Copilot:

> **Prompt:** "Continue with Wave 2 of the modernization plan for `cjemorton/simplelogin-app`. 
> Refer to `WAVE_UPGRADE_STATUS.md` and issue #40. The goal is to upgrade Flask 1.1→3.1, 
> Werkzeug 1.0→3.1, and all Flask extensions (Flask-Login, Flask-WTF, Flask-Migrate, 
> Flask-Limiter, flask-admin, flask-cors, flask-debugtoolbar, itsdangerous, MarkupSafe). 
> Update any application code as needed for API compatibility. Open a PR referencing #40."

### Key Migration Notes for Wave 2

- Flask 2.0 removed `flask.json.jsonify` import pattern changes
- Flask 2.0+ requires `app.json.provider_class` instead of `json_encoder`
- Werkzeug 2.0+ removed `werkzeug.urls.url_encode/url_decode`
- Flask-Limiter 2.0+ changed initialization API entirely
- Flask-WTF 1.0+ dropped `FlaskForm.validate_on_submit()` behavior changes
- `wtforms` 3.0 changed `StringField` validators
- `arrow` 0.16→1.3 has breaking changes in `.format()` and `.shift()`
- `bcrypt` 3→4 changed `hashpw` return types
- `python-dotenv` 0.14→1.x is mostly compatible
- `webauthn` 0.4→2.x has completely rewritten API

### Additional Packages to Upgrade in Wave 2

| Package | Current | Target | Breaking? |
|---------|---------|--------|-----------|
| flask | ~= 1.1.2 | ~= 3.1.0 | YES |
| werkzeug | ~= 1.0.1 | ~= 3.1.0 | YES |
| itsdangerous | ~= 1.1.0 | ~= 2.2.0 | YES |
| MarkupSafe | ~= 1.1.1 | ~= 3.0.0 | Minor |
| Flask-Login | ~= 0.5.0 | ~= 0.6.3 | Minor |
| Flask-WTF | ~= 0.14.3 | ~= 1.2.0 | YES |
| wtforms | ~= 2.3.3 | ~= 3.2.0 | YES |
| Flask-Migrate | ~= 2.5.3 | ~= 4.0.0 | YES |
| Flask-Limiter | == 1.5 | ~= 3.0.0 | YES |
| flask_admin | ~= 1.5.6 | ~= 1.6.0 | Minor |
| flask-cors | ~= 3.0.9 | ~= 5.0.0 | Minor |
| arrow | ~= 0.16.0 | ~= 1.3.0 | YES |
| bcrypt | ~= 3.2.0 | ~= 4.2.0 | YES |
| python-dotenv | ~= 0.14.0 | ~= 1.0.0 | Minor |
| webauthn | ~= 0.4.7 | ~= 2.0.0 | YES |
| twilio | ~= 7.3.2 | ~= 9.0.0 | YES |
| google-api-python-client | ~= 1.12.3 | ~= 2.0.0 | YES |

---

## Wave 3 — SQLAlchemy 2.0+ Migration (Not Started)

### Planned Changes

When starting Wave 3, use the following prompt with GitHub Copilot:

> **Prompt:** "Continue with Wave 3 of the modernization plan for `cjemorton/simplelogin-app`. 
> Refer to `WAVE_UPGRADE_STATUS.md` and issue #39. The goal is to migrate from SQLAlchemy 
> 1.3→2.0+, update Alembic, and refactor all ORM usage (query patterns, text() wrapping, 
> session management). Consider splitting the 135KB models.py into a models/ package. 
> Open a PR referencing #39."

### Key Migration Notes for Wave 3

- All `conn.execute("string SQL")` must become `conn.execute(text("string SQL"))`
- `Query.get()` → `Session.get(Model, id)`
- `Session.query(Model).filter_by()` patterns need review
- `engine.execute()` removed — must use `with engine.connect() as conn`
- `autocommit` behavior changed — explicit `Session.begin()` required
- Use `SQLALCHEMY_WARN_20=1` env var to find all deprecated patterns before upgrading
- `models.py` (135KB) should ideally be split into `models/` package during this wave
- `alembic` 1.4→1.14 upgrade alongside

---

## Abandoned / Problematic Dependencies (Future Consideration)

These packages have known issues but are not addressed in any wave:

| Package | Issue | Recommendation |
|---------|-------|----------------|
| `flanker` | Unmaintained (git install from mailgun/flanker) | Evaluate alternatives |
| `facebook-sdk` | Abandoned on PyPI | Remove if Facebook login unused |
| `coinbase-commerce` | Coinbase Commerce API deprecated | Remove if Coinbase payments unused |
| `PGPy` | Pinned ==0.5.4, project has low activity | Monitor; sl-pgp-rs is the replacement |
| `flask_profiler` | May not support Flask 3.x | Test in Wave 2, remove if incompatible |

---

## How to Continue

After each wave is merged, update this file:
1. Change the wave status from 🟡/⬜ to ✅
2. Fill in the PR number in the table
3. Add any gotchas or notes discovered during the upgrade
4. Use the prompt provided in the next wave's section to continue
