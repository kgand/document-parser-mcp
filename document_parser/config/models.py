"""
Configuration models using Pydantic.
"""

from typing import List, Optional
from pydantic import BaseModel, Field, field_validator


class ServerSettings(BaseModel):
    """Server configuration settings."""

    name: str = Field(default="document-parser-mcp", description="Server name")
    version: str = Field(default="1.0.0", description="Server version")
    max_concurrent_jobs: int = Field(
        default=3, ge=1, le=10, description="Maximum concurrent processing jobs"
    )
    job_timeout_seconds: int = Field(
        default=600, ge=60, description="Job timeout in seconds"
    )


class StorageSettings(BaseModel):
    """Storage configuration settings."""

    temp_directory: str = Field(
        default="./temp", description="Temporary files directory"
    )
    cleanup_interval_hours: int = Field(
        default=24, ge=1, description="Cleanup interval for temp files"
    )
    max_file_size_mb: int = Field(
        default=500, ge=1, description="Maximum file size in MB"
    )
    allowed_schemes: List[str] = Field(
        default=["http", "https", "ftp"], description="Allowed URL schemes"
    )
    download_timeout_seconds: int = Field(
        default=600, ge=30, description="Download timeout in seconds"
    )


class OCRSettings(BaseModel):
    """OCR configuration settings."""

    engine: str = Field(default="easyocr", description="OCR engine to use")
    languages: List[str] = Field(
        default=["eng"], description="Default OCR languages"
    )
    enable_auto_detect: bool = Field(
        default=True, description="Auto-detect when OCR is needed"
    )


class PDFSettings(BaseModel):
    """PDF processing settings."""

    backend: str = Field(
        default="dlparse_v4", description="PDF backend to use"
    )
    fallback_backend: str = Field(
        default="pypdfium2", description="Fallback PDF backend"
    )
    enable_table_extraction: bool = Field(
        default=True, description="Enable table extraction"
    )
    table_accuracy_mode: str = Field(
        default="accurate", description="Table extraction mode"
    )

    @field_validator("table_accuracy_mode")
    @classmethod
    def validate_table_mode(cls, value: str) -> str:
        """Validate table accuracy mode."""
        allowed = ["fast", "accurate"]
        if value not in allowed:
            raise ValueError(f"table_accuracy_mode must be one of {allowed}")
        return value


class PerformanceSettings(BaseModel):
    """Performance configuration settings."""

    max_memory_gb: int = Field(
        default=6, ge=2, description="Maximum memory usage in GB"
    )
    enable_mlx_acceleration: bool = Field(
        default=True, description="Enable MLX acceleration on Apple Silicon"
    )
    thread_count: int = Field(
        default=4, ge=1, le=16, description="Number of processing threads"
    )


class ProcessingSettings(BaseModel):
    """Document processing settings."""

    default_pipeline: str = Field(
        default="standard", description="Default processing pipeline"
    )
    enable_pipeline_auto_detect: bool = Field(
        default=True, description="Auto-detect optimal pipeline"
    )
    ocr: OCRSettings = Field(
        default_factory=OCRSettings, description="OCR settings"
    )
    pdf: PDFSettings = Field(
        default_factory=PDFSettings, description="PDF settings"
    )
    performance: PerformanceSettings = Field(
        default_factory=PerformanceSettings, description="Performance settings"
    )

    @field_validator("default_pipeline")
    @classmethod
    def validate_pipeline(cls, value: str) -> str:
        """Validate pipeline name."""
        allowed = ["standard", "vlm", "asr"]
        if value not in allowed:
            raise ValueError(f"default_pipeline must be one of {allowed}")
        return value


class LoggingSettings(BaseModel):
    """Logging configuration settings."""

    level: str = Field(default="INFO", description="Logging level")
    format_string: str = Field(
        default="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        description="Log format string",
    )
    file_path: str = Field(
        default="./logs/server.log", description="Log file path"
    )
    max_file_size_mb: int = Field(
        default=10, ge=1, description="Max log file size in MB"
    )
    backup_count: int = Field(
        default=5, ge=1, description="Number of backup log files"
    )
    enable_json_logs: bool = Field(
        default=False, description="Enable JSON formatted logs"
    )

    @field_validator("level")
    @classmethod
    def validate_level(cls, value: str) -> str:
        """Validate logging level."""
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        value_upper = value.upper()
        if value_upper not in allowed:
            raise ValueError(f"level must be one of {allowed}")
        return value_upper


class RetrySettings(BaseModel):
    """Retry configuration settings."""

    enable_pipeline_fallback: bool = Field(
        default=True, description="Enable pipeline fallback on errors"
    )
    enable_backend_fallback: bool = Field(
        default=True, description="Enable backend fallback on errors"
    )
    max_attempts: int = Field(
        default=3, ge=1, le=5, description="Maximum retry attempts"
    )
    delay_seconds: int = Field(
        default=2, ge=1, description="Delay between retries in seconds"
    )


class ApplicationSettings(BaseModel):
    """Main application settings."""

    server: ServerSettings = Field(
        default_factory=ServerSettings, description="Server settings"
    )
    storage: StorageSettings = Field(
        default_factory=StorageSettings, description="Storage settings"
    )
    processing: ProcessingSettings = Field(
        default_factory=ProcessingSettings, description="Processing settings"
    )
    logging: LoggingSettings = Field(
        default_factory=LoggingSettings, description="Logging settings"
    )
    retry: RetrySettings = Field(
        default_factory=RetrySettings, description="Retry settings"
    )

    class Config:
        """Pydantic configuration."""

        validate_assignment = True
        extra = "forbid"
