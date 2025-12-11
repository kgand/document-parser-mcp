"""
Pytest configuration and fixtures.
"""

import pytest
from pathlib import Path

from document_parser.config.models import ApplicationSettings
from document_parser.config.settings import reset_settings


@pytest.fixture
def test_settings():
    """Provide test application settings."""
    settings = ApplicationSettings()
    settings.storage.temp_directory = "./test_temp"
    settings.logging.level = "DEBUG"
    return settings


@pytest.fixture
def sample_pdf_path(tmp_path):
    """Provide path to a sample PDF file."""
    # This would need an actual PDF for integration tests
    pdf_file = tmp_path / "sample.pdf"
    pdf_file.write_text("Mock PDF content")
    return str(pdf_file)


@pytest.fixture
def mock_url():
    """Provide a mock URL."""
    return "https://example.com/document.pdf"


@pytest.fixture(autouse=True)
def reset_config():
    """Reset configuration before each test."""
    reset_settings()
    yield
    reset_settings()


@pytest.fixture
def temp_directory(tmp_path):
    """Provide a temporary directory."""
    return tmp_path
