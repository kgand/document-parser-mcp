"""
Document Parser MCP Server

A Model Context Protocol server providing intelligent document processing
capabilities using the Docling toolkit.
"""

__version__ = "1.0.0"
__author__ = "Document Parser Team"
__license__ = "MIT"

from document_parser.core.exceptions import (
    DocumentParserError,
    ProcessingError,
    ConfigurationError,
)

__all__ = [
    "__version__",
    "__author__",
    "__license__",
    "DocumentParserError",
    "ProcessingError",
    "ConfigurationError",
]
