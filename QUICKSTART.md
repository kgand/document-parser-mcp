# Quick Start Guide

Get up and running with Document Parser MCP in minutes!

## Installation

### 1. Setup Environment

```bash
# Clone repository
git clone <repository-url>
cd document-parser-mcp

# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
pip install docling
```

### 2. Optional: Enhanced Features

```bash
# For Apple Silicon MLX acceleration
pip install docling[mlx]

# For OCR support
pip install easyocr

# For tesseract OCR (macOS)
brew install tesseract
```

## First Run

### Test the Installation

```bash
# Start the server
python -m document_parser
```

The server will start and listen for MCP connections via stdio.

## Integration with Claude Desktop

### 1. Configure Claude Desktop

Edit your Claude Desktop config file:
- **macOS**: `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`

Add this configuration:

```json
{
  "mcpServers": {
    "document-parser": {
      "command": "python",
      "args": ["-m", "document_parser"],
      "cwd": "/absolute/path/to/document-parser-mcp"
    }
  }
}
```

**Important**: Replace `/absolute/path/to/document-parser-mcp` with the actual path!

### 2. Restart Claude Desktop

Close and reopen Claude Desktop completely.

### 3. Test the Integration

In a new Claude conversation, try:

```
Can you parse this document for me?
```

Then upload a PDF, DOCX, or image file. The document parser should automatically process it!

## Basic Usage Examples

### Parse a Local PDF

```json
{
  "name": "parse_document",
  "arguments": {
    "source": "/path/to/document.pdf"
  }
}
```

### Parse from URL

```json
{
  "name": "parse_document",
  "arguments": {
    "source": "https://arxiv.org/pdf/2408.09869"
  }
}
```

### Parse with Specific Pipeline

```json
{
  "name": "parse_document",
  "arguments": {
    "source": "scan.pdf",
    "pipeline": "vlm",
    "options": {
      "ocr_enabled": true
    }
  }
}
```

### Advanced Options

```json
{
  "name": "parse_document_advanced",
  "arguments": {
    "source": "document.pdf",
    "pipeline": "standard",
    "ocr_enabled": true,
    "table_accuracy_mode": "accurate",
    "pdf_backend": "dlparse_v4"
  }
}
```

## Configuration

### Create Custom Config

Copy the default configuration:

```bash
cp config.yaml my_config.yaml
```

Edit `my_config.yaml` to customize settings.

Run with custom config:

```bash
python -m document_parser --config my_config.yaml
```

### Key Settings

```yaml
# Server settings
server:
  max_concurrent_jobs: 3      # Adjust based on your RAM

# Processing settings
processing:
  default_pipeline: standard

  # OCR settings
  ocr:
    engine: easyocr
    languages: [eng]          # Add more: [eng, spa, fra]

  # Performance
  performance:
    max_memory_gb: 6          # Adjust for your system
    enable_mlx_acceleration: true  # Apple Silicon only
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'docling'"

**Solution:**
```bash
pip install docling
```

### Issue: Server doesn't appear in Claude Desktop

**Solutions:**
1. Check the config file path is correct
2. Ensure the `cwd` path is absolute, not relative
3. Restart Claude Desktop completely
4. Check server starts without errors: `python -m document_parser`

### Issue: Out of memory errors

**Solution:**
Reduce `max_concurrent_jobs` and `max_memory_gb` in config:

```yaml
server:
  max_concurrent_jobs: 1

processing:
  performance:
    max_memory_gb: 4
```

### Issue: Poor OCR quality

**Solution:**
1. Specify correct language:
```yaml
processing:
  ocr:
    languages: [eng, spa]  # Add your languages
```

2. Try different OCR engine:
```yaml
processing:
  ocr:
    engine: tesseract  # or easyocr
```

## Next Steps

- Read the [full README](README.md) for all features
- Explore [configuration options](docs/CONFIGURATION.md)
- Check [supported formats](docs/FORMATS.md)
- Run the [test suite](tests/)

## Getting Help

- Check [Troubleshooting](#troubleshooting) section above
- Review [Docling documentation](https://docling-project.github.io/docling/)
- Open an issue on GitHub

Happy parsing! 🚀
