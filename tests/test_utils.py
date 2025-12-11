"""
Tests for utility functions.
"""

import pytest
from pathlib import Path

from document_parser.utils.file_utils import (
    sanitize_filename,
    get_file_extension,
    detect_document_type,
)
from document_parser.utils.network_utils import (
    is_valid_url,
    extract_filename_from_url,
    validate_url_scheme,
)
from document_parser.utils.system_utils import generate_unique_id


class TestFileUtils:
    """Test file utility functions."""

    def test_sanitize_filename(self):
        """Test filename sanitization."""
        # Test with problematic characters
        assert sanitize_filename("file:name.pdf") == "file_name.pdf"
        assert sanitize_filename("file<>name.pdf") == "file__name.pdf"
        assert sanitize_filename('file"name.pdf') == "file_name.pdf"

    def test_get_file_extension(self):
        """Test file extension extraction."""
        assert get_file_extension("document.pdf") == ".pdf"
        assert get_file_extension("archive.tar.gz") == ".gz"
        assert get_file_extension("UPPERCASE.PDF") == ".pdf"

    def test_get_file_extension_from_url(self):
        """Test extension extraction from URL."""
        url = "https://example.com/documents/file.pdf"
        assert get_file_extension(url) == ".pdf"

    def test_detect_document_type(self):
        """Test document type detection."""
        # PDF
        doc_type, pipeline = detect_document_type("file.pdf")
        assert doc_type == "pdf"
        assert pipeline == "standard"

        # Image
        doc_type, pipeline = detect_document_type("image.png")
        assert doc_type == "image"
        assert pipeline == "vlm"

        # Audio
        doc_type, pipeline = detect_document_type("audio.mp3")
        assert doc_type == "audio"
        assert pipeline == "asr"


class TestNetworkUtils:
    """Test network utility functions."""

    def test_is_valid_url(self):
        """Test URL validation."""
        assert is_valid_url("https://example.com") is True
        assert is_valid_url("http://example.com/file.pdf") is True
        assert is_valid_url("ftp://ftp.example.com") is True
        assert is_valid_url("/local/path/file.pdf") is False
        assert is_valid_url("not a url") is False

    def test_extract_filename_from_url(self):
        """Test filename extraction from URL."""
        url = "https://example.com/documents/report.pdf"
        assert extract_filename_from_url(url) == "report.pdf"

        url = "https://example.com/"
        assert extract_filename_from_url(url) is None

    def test_validate_url_scheme(self):
        """Test URL scheme validation."""
        allowed = ["http", "https"]

        assert validate_url_scheme("https://example.com", allowed) is True
        assert validate_url_scheme("http://example.com", allowed) is True
        assert validate_url_scheme("ftp://example.com", allowed) is False


class TestSystemUtils:
    """Test system utility functions."""

    def test_generate_unique_id(self):
        """Test unique ID generation."""
        id1 = generate_unique_id()
        id2 = generate_unique_id()

        assert id1 != id2
        assert len(id1) == 8

    def test_generate_unique_id_with_prefix(self):
        """Test unique ID generation with prefix."""
        job_id = generate_unique_id("job")

        assert job_id.startswith("job_")
        assert len(job_id) > 4
