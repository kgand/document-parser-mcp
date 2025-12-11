"""
Network-related utility functions.
"""

from pathlib import Path
from urllib.parse import urlparse
from typing import Optional


def is_valid_url(source: str) -> bool:
    """
    Check if a string is a valid URL.

    Args:
        source: String to check

    Returns:
        True if valid URL, False otherwise
    """
    try:
        result = urlparse(source)
        return all([result.scheme, result.netloc])
    except Exception:
        return False


def extract_filename_from_url(url: str) -> Optional[str]:
    """
    Extract filename from a URL.

    Args:
        url: URL string

    Returns:
        Filename if found, None otherwise
    """
    try:
        parsed = urlparse(url)
        path = Path(parsed.path)
        filename = path.name

        if filename:
            return filename

        return None
    except Exception:
        return None


def validate_url_scheme(url: str, allowed_schemes: list[str]) -> bool:
    """
    Validate that URL uses an allowed scheme.

    Args:
        url: URL to validate
        allowed_schemes: List of allowed schemes (e.g., ['http', 'https'])

    Returns:
        True if scheme is allowed, False otherwise
    """
    try:
        parsed = urlparse(url)
        return parsed.scheme in allowed_schemes
    except Exception:
        return False
