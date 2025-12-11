# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-10

### Added

- Initial release of Document Parser MCP
- Core document processing engine with Docling integration
- MCP server implementation with stdio transport
- Three processing pipelines: Standard, VLM, and ASR
- Intelligent pipeline auto-detection based on file type
- Job queue system for concurrent processing
- Task tracking and monitoring
- Configuration system with YAML support
- Support for multiple document formats:
  - PDF documents
  - Office files (DOCX, XLSX, PPTX)
  - Images (PNG, JPEG, TIFF, BMP, WEBP)
  - Audio files (MP3, WAV, M4A, FLAC)
  - HTML and Markdown
  - CSV and XML
- Five MCP tools:
  - `parse_document`: Basic document parsing
  - `parse_document_advanced`: Advanced parsing with detailed options
  - `get_job_status`: Job status monitoring
  - `list_supported_formats`: Format listing
  - `get_queue_statistics`: Queue and processing statistics
- Comprehensive test suite with pytest
- CLI entry point for running the server
- MLX acceleration support for Apple Silicon
- OCR support with multiple engines (EasyOCR, Tesseract)
- Automatic file cleanup and resource management
- Download manager for processing remote URLs
- Extensive documentation:
  - README with features and usage
  - Quick start guide
  - Contributing guidelines
  - Configuration examples

### Configuration

- Flexible YAML-based configuration
- Environment variable support
- Validation with Pydantic models
- Default configuration file included

### Developer Experience

- Type hints throughout codebase
- Comprehensive docstrings
- Black code formatting
- Ruff linting
- pytest test framework
- Code coverage reporting
- Development requirements file

### Performance

- Concurrent job processing
- Memory management controls
- MLX acceleration for Apple Silicon
- Efficient file handling
- Background cleanup tasks

### Documentation

- Comprehensive README
- Quick start guide
- Contributing guidelines
- Inline code documentation
- Configuration examples
- Troubleshooting guides

## [Unreleased]

### Planned

- Additional processing pipeline options
- Enhanced error recovery mechanisms
- Performance optimizations
- Extended format support
- Batch processing capabilities
- Web UI for monitoring
- Docker containerization
- More comprehensive examples

---

## Release Notes

### Version 1.0.0

This is the first stable release of Document Parser MCP. The server provides a robust foundation for document processing through the Model Context Protocol, with support for a wide variety of document formats and processing options.

Key highlights:
- Production-ready MCP server
- Multiple processing pipelines
- Comprehensive format support
- Extensive test coverage
- Full documentation

We welcome contributions and feedback from the community!
