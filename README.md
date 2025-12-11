# Document Parser MCP

A Model Context Protocol (MCP) server that provides intelligent document parsing and conversion capabilities using the Docling toolkit. Convert any document (PDF, DOCX, images, audio, etc.) into clean Markdown for AI processing and RAG pipelines.

## Features

- **Universal Document Support**: PDFs, Office documents (DOCX/XLSX/PPTX), images, HTML, Markdown, audio files, and more
- **Multiple Processing Pipelines**:
  - Standard: Fast, high-quality conversion with advanced layout analysis
  - VLM: Vision-language models for complex layouts and handwritten content
  - ASR: Automatic speech recognition for audio transcription
- **Intelligent Auto-Detection**: Automatically selects optimal pipeline based on file type
- **Concurrent Processing**: Built-in job queue for handling multiple requests
- **MCP Integration**: Seamless integration with Claude Desktop and other MCP clients
- **Clean Markdown Output**: High-quality structured text ready for AI consumption

## Installation

### Prerequisites

- Python 3.9 or higher
- 8GB+ RAM recommended

### Quick Start

1. **Clone the repository:**
```bash
git clone <repository-url>
cd document-parser-mcp
```

2. **Create virtual environment:**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

4. **Install Docling with optional features:**
```bash
# Core Docling
pip install docling

# For Apple Silicon MLX acceleration
pip install docling[mlx]

# Optional OCR engines
pip install easyocr
```

## Usage

### Running the Server

Start the MCP server:

```bash
python -m document_parser
```

With custom configuration:

```bash
python -m document_parser --config /path/to/config.yaml
```

With debug logging:

```bash
python -m document_parser --debug
```

### Configuration

The server is configured via `config.yaml`. Key settings:

```yaml
server:
  name: document-parser-mcp
  max_concurrent_jobs: 3
  job_timeout_seconds: 600

processing:
  default_pipeline: standard
  enable_pipeline_auto_detect: true

  ocr:
    engine: easyocr
    languages: [eng]

  pdf:
    backend: dlparse_v4
    table_accuracy_mode: accurate
```

See [Configuration Guide](docs/CONFIGURATION.md) for detailed options.

## MCP Tools

The server provides the following MCP tools:

### `parse_document`

Parse any document to Markdown.

**Parameters:**
- `source` (required): File path or URL to the document
- `pipeline` (optional): Processing pipeline - `standard`, `vlm`, or `asr`
- `options` (optional): Additional processing options

**Example:**
```json
{
  "name": "parse_document",
  "arguments": {
    "source": "https://arxiv.org/pdf/2408.09869",
    "pipeline": "standard"
  }
}
```

### `parse_document_advanced`

Advanced parsing with detailed configuration.

**Parameters:**
- `source` (required): File path or URL
- `pipeline` (optional): Processing pipeline
- `ocr_enabled` (optional): Enable/disable OCR
- `table_accuracy_mode` (optional): `fast` or `accurate`
- `pdf_backend` (optional): PDF processing backend
- `enable_enrichments` (optional): Enable code/formula enrichments

### `get_job_status`

Get the status of a processing job.

**Parameters:**
- `job_id` (required): Job identifier

### `list_supported_formats`

List all supported input formats and pipelines.

### `get_queue_statistics`

Get current queue and processing statistics.

## Integration with Claude Desktop

Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "document-parser": {
      "command": "python",
      "args": ["-m", "document_parser"],
      "cwd": "/path/to/document-parser-mcp"
    }
  }
}
```

Restart Claude Desktop and the document parser will be available as a tool.

## Pipeline Selection Guide

### Standard Pipeline (Default)
- **Best for**: Born-digital PDFs, Office documents, clean layouts
- **Features**: Advanced layout analysis, table structure recovery, optional OCR
- **Performance**: Fast, memory-efficient

### VLM Pipeline
- **Best for**: Complex layouts, handwritten notes, screenshots, scanned documents
- **Features**: Vision-language model processing, end-to-end page understanding
- **Performance**: Slower, MLX-accelerated on Apple Silicon

### ASR Pipeline
- **Best for**: Audio files (meetings, lectures, interviews)
- **Features**: Whisper-based transcription
- **Performance**: CPU/GPU intensive

## Development

### Running Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run with coverage
pytest --cov=document_parser
```

### Code Quality

```bash
# Format code
black document_parser tests

# Lint
ruff check document_parser tests

# Type checking
mypy document_parser
```

## Project Structure

```
document-parser-mcp/
├── document_parser/         # Main package
│   ├── config/             # Configuration system
│   ├── core/               # Core exceptions and types
│   ├── engine/             # Document processing engine
│   ├── mcp/                # MCP server implementation
│   ├── processing/         # Job queue and tracking
│   └── utils/              # Utility functions
├── tests/                  # Test suite
├── config.yaml            # Default configuration
├── requirements.txt       # Production dependencies
└── setup.py              # Package configuration
```

## Performance Optimization

### Memory Management
- Configure `max_memory_gb` for your system
- Set `max_concurrent_jobs` based on available resources
- Large files are processed with automatic cleanup

### MLX Acceleration (Apple Silicon)
- Install with `pip install docling[mlx]`
- Enable in config: `enable_mlx_acceleration: true`
- Automatic fallback to CPU if unavailable

## Troubleshooting

### Common Issues

**"ModuleNotFoundError: No module named 'docling'"**
```bash
pip install docling
```

**Queue is full errors**
- Wait for current jobs to complete
- Increase `max_concurrent_jobs` in config

**Memory errors with large files**
- Reduce `max_memory_gb` in config
- Use `pipeline: standard` instead of `vlm`

**OCR not working**
```bash
pip install easyocr
# Or for tesseract
brew install tesseract  # macOS
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with [Docling](https://github.com/docling-project/docling) - an amazing document understanding toolkit
- Uses the [Model Context Protocol](https://modelcontextprotocol.io) for AI integration

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/document-parser-mcp/issues)
- **Documentation**: [Full Documentation](docs/)
