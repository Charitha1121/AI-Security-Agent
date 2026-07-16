"""Reusable logging helpers for the FastAPI backend.

This module provides a small, production-friendly logger factory that gives each
module a consistent console logger while respecting the application's configured
log level.
"""

import logging
import sys
from typing import Final

from app.core.config import settings

# Shared log format used by all console handlers.
DEFAULT_LOG_FORMAT: Final[str] = "%(asctime)s | %(levelname)s | %(name)s | %(message)s"


def get_logger(name: str) -> logging.Logger:
    """Return a configured logger for the given module name.

    The logger reads its level from application settings and attaches a single
    console handler to avoid duplicate output when the function is called more
    than once for the same logger name.
    """

    logger = logging.getLogger(name)
    logger.setLevel(getattr(logging, settings.LOG_LEVEL, logging.INFO))

    # Reuse an existing handler set to prevent duplicate console logging.
    if logger.handlers:
        return logger

    # Attach a console handler so logs are visible in local development and
    # containerized environments.
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(logging.Formatter(DEFAULT_LOG_FORMAT))
    logger.addHandler(handler)

    # Prevent log records from bubbling up to the root logger and producing
    # duplicate entries.
    logger.propagate = False

    return logger
