"""
Core module for document parser functionality.
"""

from document_parser.core.exceptions import (
    ConfigurationError,
    DocumentParserError,
    ProcessingError,
)

__all__ = [
    "DocumentParserError",
    "ProcessingError",
    "ConfigurationError",
]
