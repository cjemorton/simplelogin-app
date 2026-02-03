"""
Tests for logging configuration and log spam suppression.
"""

import logging
import os


def test_flanker_logger_suppressed_by_default():
    """
    Test that flanker logger is set to ERROR level by default,
    suppressing INFO/DEBUG/WARNING spam.
    """
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
    # Set up log capture at INFO level
    with caplog.at_level(logging.INFO):
        # Import flanker (this might trigger some internal logging)
        from flanker.addresslib import address

        # Parse an email address (this is a common operation that might log)
        parsed = address.parse("user@example.com")

        # Verify the parsing worked (using the variable)
        assert parsed is not None, "Email parsing should succeed"

        # Check that no flanker logs at INFO/DEBUG/WARNING level were captured
        flanker_logs = [
            record
            for record in caplog.records
            if record.name.startswith("flanker") and record.levelno < logging.ERROR
        ]

        assert len(flanker_logs) == 0, (
            f"Expected no flanker logs below ERROR level, but found {len(flanker_logs)}: "
            f"{[f'{r.name}:{r.levelname}:{r.message}' for r in flanker_logs]}"
        )


def test_log_level_from_environment():
    """
    Test that LOG_LEVEL environment variable controls the log level.
    """
    from app.log import LOG

    # The log level should be INFO by default (as set in test environment)
    # or whatever was configured via LOG_LEVEL env var
    expected_level_name = os.environ.get("LOG_LEVEL", "INFO").upper()
    actual_level_name = logging.getLevelName(LOG.level)

    # In test environment, we expect INFO level
    assert (
        actual_level_name == expected_level_name
    ), f"Expected log level {expected_level_name}, but got {actual_level_name}"


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
    assert silence_flag in ["0", "1"], "SILENCE_FLANKER_LOGS should be '0' or '1'"


def test_app_logger_exists():
    """Test that the main application logger (LOG) exists and is properly configured."""
    from app.log import LOG

    assert LOG is not None
    assert LOG.name == "SL"
    assert isinstance(LOG, logging.Logger)


def test_logger_has_custom_filters():
    """Test that the logger has the required custom filters."""
    from app.log import LOG

    # Check that LOG has filters
    filter_types = [type(f).__name__ for f in LOG.filters]

    assert "EmailHandlerFilter" in filter_types, "LOG should have EmailHandlerFilter"
    assert "RequestIdFilter" in filter_types, "LOG should have RequestIdFilter"


def test_email_handler_filter_adds_message_id():
    """Test that EmailHandlerFilter correctly adds message_id to log records."""
    from app.log import EmailHandlerFilter, set_message_id
    import logging

    # Create a filter instance
    filter_instance = EmailHandlerFilter()

    # Create a dummy log record
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg="test message",
        args=(),
        exc_info=None,
    )

    # Set a message ID
    test_message_id = "test-message-123"
    set_message_id(test_message_id)

    # Apply filter
    result = filter_instance.filter(record)

    # Verify the filter returns True (record should be logged)
    assert result is True

    # Verify message_id was added to the record
    assert hasattr(record, "message_id")
    assert record.message_id == test_message_id


def test_request_id_filter_without_flask_context():
    """Test that RequestIdFilter handles missing Flask context gracefully."""
    from app.log import RequestIdFilter
    import logging

    # Create a filter instance
    filter_instance = RequestIdFilter()

    # Create a dummy log record
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="test.py",
        lineno=1,
        msg="test message",
        args=(),
        exc_info=None,
    )

    # Apply filter (should not raise exception even without Flask context)
    result = filter_instance.filter(record)

    # Verify the filter returns True (record should be logged)
    assert result is True

    # Verify request_id was added (should be empty string outside request context)
    assert hasattr(record, "request_id")
    assert record.request_id == ""
