"""
Custom exceptions for the document parser.
"""


class DocumentParserError(Exception):
    """Base exception for all document parser errors."""

    def __init__(self, message: str, details: str = None):
        self.message = message
        self.details = details
        super().__init__(self.message)

    def __str__(self):
        if self.details:
            return f"{self.message}: {self.details}"
        return self.message


class ProcessingError(DocumentParserError):
    """Raised when document processing fails."""

    pass


class ConfigurationError(DocumentParserError):
    """Raised when configuration is invalid or missing."""

    pass


class NetworkError(DocumentParserError):
    """Raised when network operations fail."""

    pass


class ValidationError(DocumentParserError):
    """Raised when input validation fails."""

    pass
