import sys
from typing import Optional

import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from sentry_sdk.integrations.sqlalchemy import SqlalchemyIntegration
from sentry_sdk.types import Event, Hint

from app.log import LOG

_HTTP_CODES_TO_IGNORE = [416]


def _should_send(_event: Event, hint: Hint) -> bool:
    # Check if this is an HTTP Exception event
    if "exc_info" in hint:
        exc_type, exc_value, exc_traceback = hint["exc_info"]
        # Check if it's a Werkzeug HTTPException (raised for HTTP status codes)
        if hasattr(exc_value, "code") and exc_value.code in _HTTP_CODES_TO_IGNORE:
            return False
    return True


def sentry_before_send(event: Event, hint: Hint) -> Optional[Event]:
    if _should_send(event, hint):
        return event
    return None


def init_sentry(
    sentry_dsn: Optional[str],
    skip_sentry: bool,
    sha1: str,
    trace_rate: float,
    require_sentry: bool = False,
) -> None:
    """
    Initialize Sentry with the following rules:

    1. If BOTH SKIP_SENTRY=1 and SENTRY_DSN are set:
       - SENTRY_DSN takes precedence, and Sentry is initialized.
       - Log a warning message explaining the precedence.

    2. If ONLY SKIP_SENTRY=1 is set (and SENTRY_DSN is not set):
       - Sentry initialization is skipped (silent).

    3. If ONLY SENTRY_DSN is set:
       - Sentry is initialized normally.

    4. If NEITHER SKIP_SENTRY nor SENTRY_DSN are set:
       - If require_sentry is True: Log an error and exit immediately to prevent wasted build time.
       - If require_sentry is False: Skip initialization silently (for development/test environments).

    Args:
        sentry_dsn: The Sentry DSN URL (from SENTRY_DSN env var)
        skip_sentry: Whether SKIP_SENTRY=1 is set
        sha1: The git SHA1 for release tagging
        trace_rate: The Sentry trace sample rate
        require_sentry: If True, exit when neither SKIP_SENTRY nor SENTRY_DSN are set
    """
    # Rule 1: Both SKIP_SENTRY and SENTRY_DSN are set
    if skip_sentry and sentry_dsn:
        LOG.warning(
            "SKIP_SENTRY is set, but SENTRY_DSN is taking precedence. "
            "To disable Sentry, unset SENTRY_DSN."
        )
        _initialize_sentry_sdk(sentry_dsn, sha1, trace_rate)
        return

    # Rule 2: Only SKIP_SENTRY is set (no SENTRY_DSN)
    if skip_sentry and not sentry_dsn:
        # Skip Sentry initialization silently
        return

    # Rule 3: Only SENTRY_DSN is set
    if sentry_dsn and not skip_sentry:
        LOG.debug("Initializing Sentry")
        _initialize_sentry_sdk(sentry_dsn, sha1, trace_rate)
        return

    # Rule 4: Neither SKIP_SENTRY nor SENTRY_DSN are set
    if not skip_sentry and not sentry_dsn:
        if require_sentry:
            LOG.error(
                "CRITICAL: Sentry cannot be initialized. "
                "Either set SENTRY_DSN to enable Sentry, or set SKIP_SENTRY=1 to skip initialization. "
                "Stopping the build immediately to prevent wasted build time."
            )
            sys.exit(1)
        else:
            # For development/test environments, skip silently
            return


def _initialize_sentry_sdk(sentry_dsn: str, sha1: str, trace_rate: float) -> None:
    """Helper function to actually initialize the Sentry SDK."""
    sentry_sdk.init(
        dsn=sentry_dsn,
        release=f"app@{sha1}",
        integrations=[
            FlaskIntegration(),
            SqlalchemyIntegration(),
        ],
        before_send=sentry_before_send,
        traces_sample_rate=trace_rate,
    )
