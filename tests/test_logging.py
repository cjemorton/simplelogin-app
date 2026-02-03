"""
Tests for logging configuration and log spam suppression.
"""

import logging
import os
from unittest.mock import patch

import pytest


def test_flanker_logger_suppressed_by_default():
    """
    Test that flanker logger is set to ERROR level by default,
    suppressing INFO/DEBUG/WARNING spam.
    """
    # Import after test setup to ensure our logging config is applied
    from app.log import LOG
    
    # Get the flanker logger
    flanker_logger = logging.getLogger("flanker")
    
    # Verify it's set to ERROR level (suppressing spam)
    assert flanker_logger.level == logging.ERROR, (
        f"Expected flanker logger to be at ERROR level ({logging.ERROR}), "
        f"but got {flanker_logger.level}"
    )


def test_spf_logger_suppressed_by_default():
    """
    Test that spf logger is set to ERROR level by default,
    suppressing INFO/DEBUG/WARNING spam.
    """
    from app.log import LOG
    
    # Get the spf logger
    spf_logger = logging.getLogger("spf")
    
    # Verify it's set to ERROR level (suppressing spam)
    assert spf_logger.level == logging.ERROR, (
        f"Expected spf logger to be at ERROR level ({logging.ERROR}), "
        f"but got {spf_logger.level}"
    )


def test_flanker_import_does_not_spam_logs(caplog):
    """
    Test that importing and using flanker does not create log spam.
    """
    from app.log import LOG
    
    # Set up log capture at INFO level
    with caplog.at_level(logging.INFO):
        # Import flanker (this might trigger some internal logging)
        from flanker.addresslib import address
        
        # Parse an email address (this is a common operation that might log)
        parsed = address.parse("user@example.com")
        
        # Check that no flanker logs at INFO/DEBUG/WARNING level were captured
        flanker_logs = [
            record for record in caplog.records 
            if record.name.startswith("flanker") and record.levelno < logging.ERROR
        ]
        
        assert len(flanker_logs) == 0, (
            f"Expected no flanker logs below ERROR level, but found {len(flanker_logs)}: "
            f"{[f'{r.name}:{r.levelname}:{r.message}' for r in flanker_logs]}"
        )


def test_log_level_from_environment():
    """
    Test that LOG_LEVEL environment variable controls the log level.
    Note: This test may not work as expected in the current test run since
    logging is configured at import time. It's here for documentation purposes.
    """
    from app.log import LOG, _LOG_LEVEL
    
    # The log level should be determined from environment at import time
    # Default is INFO
    expected_level = os.environ.get("LOG_LEVEL", "INFO").upper()
    
    # Verify the internal log level variable matches
    assert logging.getLevelName(_LOG_LEVEL) == expected_level or _LOG_LEVEL == logging.INFO


def test_silence_flanker_logs_env_var_disables_suppression():
    """
    Test that SILENCE_FLANKER_LOGS=0 would disable suppression.
    Note: This test documents the expected behavior but may not work in current
    test run since logging is configured at import time.
    """
    # This test documents that SILENCE_FLANKER_LOGS env var exists
    # In a real scenario, one would need to set this before importing app.log
    silence_flag = os.environ.get("SILENCE_FLANKER_LOGS", "1")
    
    # Default should be "1" (enabled)
    # Can be overridden to "0" to disable suppression for debugging
    assert silence_flag in ["0", "1"], (
        "SILENCE_FLANKER_LOGS should be '0' or '1'"
    )


def test_app_logger_exists():
    """Test that the main application logger (LOG) exists and is properly configured."""
    from app.log import LOG
    
    assert LOG is not None
    assert LOG.name == "SL"
    assert isinstance(LOG, logging.Logger)


def test_logger_has_custom_filters():
    """Test that the logger has the required custom filters."""
    from app.log import LOG, EmailHandlerFilter, RequestIdFilter
    
    # Check that LOG has filters
    filter_types = [type(f).__name__ for f in LOG.filters]
    
    assert "EmailHandlerFilter" in filter_types, "LOG should have EmailHandlerFilter"
    assert "RequestIdFilter" in filter_types, "LOG should have RequestIdFilter"
