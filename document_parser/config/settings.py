"""
Settings loader and manager.
"""

import os
from pathlib import Path
from typing import Optional

import yaml

from document_parser.config.models import ApplicationSettings
from document_parser.core.exceptions import ConfigurationError

_settings_instance: Optional[ApplicationSettings] = None


def load_settings(config_path: Optional[str] = None) -> ApplicationSettings:
    """
    Load application settings from YAML file.

    Args:
        config_path: Path to configuration file. If None, uses default config.yaml

    Returns:
        ApplicationSettings instance

    Raises:
        ConfigurationError: If configuration is invalid
    """
    # Use default if no path provided
    if config_path is None:
        config_path = os.getenv("DOCUMENT_PARSER_CONFIG", "config.yaml")

    config_file = Path(config_path)

    # Return default settings if file doesn't exist
    if not config_file.exists():
        return ApplicationSettings()

    try:
        with open(config_file, encoding="utf-8") as f:
            config_data = yaml.safe_load(f)

        if config_data is None:
            return ApplicationSettings()

        return ApplicationSettings(**config_data)

    except yaml.YAMLError as e:
        raise ConfigurationError(
            f"Failed to parse YAML configuration: {config_path}", details=str(e)
        )
    except Exception as e:
        raise ConfigurationError(
            f"Failed to load configuration: {config_path}", details=str(e)
        )


def get_settings() -> ApplicationSettings:
    """
    Get singleton settings instance.

    Returns:
        ApplicationSettings instance
    """
    global _settings_instance

    if _settings_instance is None:
        _settings_instance = load_settings()

    return _settings_instance


def reset_settings() -> None:
    """
    Reset settings singleton (useful for testing).
    """
    global _settings_instance
    _settings_instance = None


def create_default_config(output_path: str = "config.yaml") -> None:
    """
    Create a default configuration file.

    Args:
        output_path: Path where to write the config file
    """
    settings = ApplicationSettings()

    config_dict = {
        "server": {
            "name": settings.server.name,
            "version": settings.server.version,
            "max_concurrent_jobs": settings.server.max_concurrent_jobs,
            "job_timeout_seconds": settings.server.job_timeout_seconds,
        },
        "storage": {
            "temp_directory": settings.storage.temp_directory,
            "cleanup_interval_hours": settings.storage.cleanup_interval_hours,
            "max_file_size_mb": settings.storage.max_file_size_mb,
            "allowed_schemes": settings.storage.allowed_schemes,
            "download_timeout_seconds": settings.storage.download_timeout_seconds,
        },
        "processing": {
            "default_pipeline": settings.processing.default_pipeline,
            "enable_pipeline_auto_detect": settings.processing.enable_pipeline_auto_detect,
            "ocr": {
                "engine": settings.processing.ocr.engine,
                "languages": settings.processing.ocr.languages,
                "enable_auto_detect": settings.processing.ocr.enable_auto_detect,
            },
            "pdf": {
                "backend": settings.processing.pdf.backend,
                "fallback_backend": settings.processing.pdf.fallback_backend,
                "enable_table_extraction": settings.processing.pdf.enable_table_extraction,
                "table_accuracy_mode": settings.processing.pdf.table_accuracy_mode,
            },
            "performance": {
                "max_memory_gb": settings.processing.performance.max_memory_gb,
                "enable_mlx_acceleration": settings.processing.performance.enable_mlx_acceleration,
                "thread_count": settings.processing.performance.thread_count,
            },
        },
        "logging": {
            "level": settings.logging.level,
            "format_string": settings.logging.format_string,
            "file_path": settings.logging.file_path,
            "max_file_size_mb": settings.logging.max_file_size_mb,
            "backup_count": settings.logging.backup_count,
            "enable_json_logs": settings.logging.enable_json_logs,
        },
        "retry": {
            "enable_pipeline_fallback": settings.retry.enable_pipeline_fallback,
            "enable_backend_fallback": settings.retry.enable_backend_fallback,
            "max_attempts": settings.retry.max_attempts,
            "delay_seconds": settings.retry.delay_seconds,
        },
    }

    output_file = Path(output_path)
    with open(output_file, "w", encoding="utf-8") as f:
        yaml.dump(
            config_dict,
            f,
            default_flow_style=False,
            sort_keys=False,
            indent=2,
        )
