"""
Logging configuration for IntelliICU.

Provides centralized structured logging using Structlog.
"""

import logging
import sys

try:
    import structlog
except ImportError:
    structlog = None


def configure_logging() -> None:
    """
    Configure application-wide structured logging.
    """

    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.INFO,
    )

    if structlog is not None:
        structlog.configure(
            processors=[
                structlog.contextvars.merge_contextvars,
                structlog.processors.TimeStamper(fmt="iso"),
                structlog.processors.add_log_level,
                structlog.processors.JSONRenderer(),
            ],
            logger_factory=structlog.stdlib.LoggerFactory(),
            cache_logger_on_first_use=True,
        )


logger = structlog.get_logger() if structlog is not None else logging.getLogger("intelliicu")