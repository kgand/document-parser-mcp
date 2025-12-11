"""
Tests for configuration system.
"""

import pytest
from pathlib import Path

from document_parser.config.models import (
    ApplicationSettings,
    LoggingSettings,
    ProcessingSettings,
)
from document_parser.config.settings import load_settings


class TestConfigurationModels:
    """Test configuration models."""

    def test_default_application_settings(self):
        """Test default application settings."""
        settings = ApplicationSettings()

        assert settings.server.name == "document-parser-mcp"
        assert settings.server.max_concurrent_jobs == 3
        assert settings.processing.default_pipeline == "standard"

    def test_logging_level_validation(self):
        """Test logging level validation."""
        # Valid levels
        for level in ["DEBUG", "INFO", "WARNING", "ERROR"]:
            settings = LoggingSettings(level=level)
            assert settings.level == level

        # Invalid level should raise error
        with pytest.raises(ValueError):
            LoggingSettings(level="INVALID")

    def test_pipeline_validation(self):
        """Test pipeline validation."""
        # Valid pipeline
        settings = ProcessingSettings(default_pipeline="vlm")
        assert settings.default_pipeline == "vlm"

        # Invalid pipeline
        with pytest.raises(ValueError):
            ProcessingSettings(default_pipeline="invalid")

    def test_table_mode_validation(self):
        """Test table mode validation."""
        settings = ProcessingSettings()

        # Valid modes
        settings.pdf.table_accuracy_mode = "fast"
        assert settings.pdf.table_accuracy_mode == "fast"

        # Invalid mode should raise error
        with pytest.raises(ValueError):
            settings.pdf.table_accuracy_mode = "invalid"


class TestConfigurationLoading:
    """Test configuration loading."""

    def test_load_default_settings(self):
        """Test loading default settings when no config file exists."""
        settings = load_settings("nonexistent.yaml")
        assert isinstance(settings, ApplicationSettings)

    def test_settings_singleton(self):
        """Test settings singleton behavior."""
        from document_parser.config.settings import get_settings, reset_settings

        reset_settings()

        settings1 = get_settings()
        settings2 = get_settings()

        assert settings1 is settings2

        reset_settings()
