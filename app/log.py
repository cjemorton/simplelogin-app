import logging
import os
import sys
import time
import warnings

import coloredlogs

from app.config import (
    COLOR_LOG,
)

# Suppress SyntaxWarnings from dependencies
# Some third-party libraries (e.g., older versions of libraries) may trigger
# SyntaxWarnings that are not relevant to our application code. These are typically
# safe to suppress in production environments.
warnings.filterwarnings("ignore", category=SyntaxWarning)

# Determine log level from environment
# Default to INFO for production, can override with LOG_LEVEL env var
_LOG_LEVEL_STR = os.environ.get("LOG_LEVEL", "INFO").upper()
_LOG_LEVEL = getattr(logging, _LOG_LEVEL_STR, logging.INFO)

# this format allows clickable link to code source in PyCharm
_log_format = (
    "%(asctime)s - %(name)s - %(levelname)s - %(process)d - %(request_id)s"
    '"%(pathname)s:%(lineno)d" - %(funcName)s() - %(message_id)s - %(message)s'
)
_log_formatter = logging.Formatter(_log_format)

# used to keep track of an email lifecycle
_MESSAGE_ID = ""


def set_message_id(message_id):
    global _MESSAGE_ID
    LOG.d("set message_id %s", message_id)
    _MESSAGE_ID = message_id


class EmailHandlerFilter(logging.Filter):
    """automatically add message-id to keep track of an email processing"""

    def filter(self, record):
        message_id = self.get_message_id()
        record.message_id = message_id if message_id else ""
        return True

    def get_message_id(self):
        return _MESSAGE_ID


class RequestIdFilter(logging.Filter):
    """automatically add request-id to keep track of a request"""

    def filter(self, record):
        from flask import g, has_request_context

        request_id = ""
        if has_request_context() and hasattr(g, "request_id"):
            ctx_request_id = getattr(g, "request_id")
            if ctx_request_id:
                request_id = f"{ctx_request_id} - "
        record.request_id = request_id
        return True


def _get_console_handler():
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(_log_formatter)
    console_handler.formatter.converter = time.gmtime

    return console_handler


def _get_logger(name) -> logging.Logger:
    logger = logging.getLogger(name)

    logger.setLevel(_LOG_LEVEL)

    # leave the handlers level at NOTSET so the level checking is only handled by the logger
    logger.addHandler(_get_console_handler())

    logger.addFilter(EmailHandlerFilter())
    logger.addFilter(RequestIdFilter())

    # no propagation to avoid propagating to root logger
    logger.propagate = False

    if COLOR_LOG:
        coloredlogs.install(level=_LOG_LEVEL, logger=logger, fmt=_log_format)

    return logger


# Suppress log spam from library dependencies
# This must happen before any imports that use these libraries
_SILENCE_FLANKER_LOGS = os.environ.get("SILENCE_FLANKER_LOGS", "1") == "1"
if _SILENCE_FLANKER_LOGS:
    # Set flanker logger to ERROR to suppress INFO/DEBUG/WARNING spam
    flanker_logger = logging.getLogger("flanker")
    flanker_logger.setLevel(logging.ERROR)
    
    # Set spf logger to ERROR to suppress INFO/DEBUG/WARNING spam
    spf_logger = logging.getLogger("spf")
    spf_logger.setLevel(logging.ERROR)


# Disable flask logs such as 127.0.0.1 - - [15/Feb/2013 10:52:22] "GET /index.html HTTP/1.1" 200
log = logging.getLogger("werkzeug")
log.disabled = True

# Set some shortcuts
logging.Logger.d = logging.Logger.debug
logging.Logger.i = logging.Logger.info
logging.Logger.w = logging.Logger.warning
logging.Logger.e = logging.Logger.exception

LOG = _get_logger("SL")
