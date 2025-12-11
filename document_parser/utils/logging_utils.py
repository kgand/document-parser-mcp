"""
Logging configuration utilities.
"""

import logging
import logging.handlers
from pathlib import Path
from typing import Optional

from document_parser.config.models import LoggingSettings


def setup_logging(settings: LoggingSettings) -> None:
    """
    Configure application logging based on settings.

    Args:
        settings: Logging configuration settings
    """
    # Ensure log directory exists
    log_file = Path(settings.file_path)
    log_file.parent.mkdir(parents=True, exist_ok=True)

    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, settings.level))

    # Clear existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Create formatters
    if settings.enable_json_logs:
        try:
            from pythonjsonlogger import jsonlogger

            formatter = jsonlogger.JsonFormatter(
                "%(asctime)s %(name)s %(levelname)s %(message)s"
            )
        except ImportError:
            # Fallback to standard formatter if json logger not available
            formatter = logging.Formatter(settings.format_string)
    else:
        formatter = logging.Formatter(settings.format_string)

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, settings.level))
    console_handler.setFormatter(formatter)
    root_logger.addHandler(console_handler)

    # File handler with rotation
    file_handler = logging.handlers.RotatingFileHandler(
        log_file,
        maxBytes=settings.max_file_size_mb * 1024 * 1024,
        backupCount=settings.backup_count,
    )
    file_handler.setLevel(getattr(logging, settings.level))
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """
    Get a logger instance.

    Args:
        name: Logger name (defaults to __name__ of caller)

    Returns:
        Logger instance
    """
    return logging.getLogger(name)
