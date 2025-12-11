# API Reference

## MCP Tools

### parse_document

Parse and convert any document to Markdown format.

**Input Schema:**
```json
{
  "source": "string (required)",
  "pipeline": "string (optional: standard|vlm|asr|auto)",
  "options": {
    "ocr_enabled": "boolean",
    "ocr_language": "string",
    "table_accuracy_mode": "string (fast|accurate)",
    "pdf_backend": "string (dlparse_v4|pypdfium2)",
    "enable_enrichments": "boolean"
  }
}
```

**Returns:** Markdown text

**Example:**
```json
{
  "name": "parse_document",
  "arguments": {
    "source": "/path/to/document.pdf",
    "pipeline": "standard"
  }
}
```

### parse_document_advanced

Advanced document parsing with detailed configuration options.

**Input Schema:**
```json
{
  "source": "string (required)",
  "pipeline": "string (optional)",
  "ocr_enabled": "boolean",
  "ocr_language": "string",
  "table_accuracy_mode": "string",
  "pdf_backend": "string",
  "enable_enrichments": "boolean"
}
```

**Returns:** Markdown text

### get_job_status

Get the status of a processing job.

**Input Schema:**
```json
{
  "job_id": "string (required)"
}
```

**Returns:** Job status JSON

**Response Format:**
```json
{
  "job_id": "string",
  "source_path": "string",
  "pipeline": "string",
  "status": "string",
  "created_at": "ISO8601 timestamp",
  "started_at": "ISO8601 timestamp",
  "completed_at": "ISO8601 timestamp",
  "duration_seconds": "number",
  "retry_count": "number",
  "error_message": "string"
}
```

### list_supported_formats

List all supported input formats and processing pipelines.

**Input Schema:**
```json
{}
```

**Returns:** Supported formats JSON

**Response Format:**
```json
{
  "input_formats": ["pdf", "docx", ...],
  "output_formats": ["markdown", "html", "json", "text", "doctags"],
  "pipelines": ["standard", "vlm", "asr"]
}
```

### get_queue_statistics

Get current queue and processing statistics.

**Input Schema:**
```json
{}
```

**Returns:** Statistics JSON

**Response Format:**
```json
{
  "queue": {
    "current_size": "number",
    "max_size": "number",
    "is_full": "boolean",
    "is_empty": "boolean"
  },
  "processing": {
    "total_jobs": "number",
    "active_jobs": "number",
    "status_counts": {
      "pending": "number",
      "running": "number",
      "completed": "number",
      "failed": "number"
    },
    "average_duration_seconds": "number"
  }
}
```

## Python API

### DocumentProcessor

Main document processing engine.

```python
from document_parser.engine.processor import DocumentProcessor
from document_parser.config.settings import get_settings

# Initialize
settings = get_settings()
processor = DocumentProcessor(settings)

# Process document
result = await processor.process_document(
    source="document.pdf",
    pipeline="standard",
    options={"ocr_enabled": True}
)
```

#### Methods

**`async process_document(source, pipeline=None, options=None)`**

Process a document and return Markdown.

- **source** (str): File path or URL
- **pipeline** (str, optional): Processing pipeline
- **options** (dict, optional): Processing options
- **Returns**: str - Markdown content

**`get_supported_formats()`**

Get list of supported formats.

- **Returns**: dict - Supported formats

### DocumentParserServer

MCP server implementation.

```python
from document_parser.mcp.server import DocumentParserServer
from document_parser.config.settings import load_settings

# Initialize
settings = load_settings("config.yaml")
server = DocumentParserServer(settings)

# Run server
await server.run()
```

## Configuration API

### ApplicationSettings

Main configuration model.

```python
from document_parser.config.models import ApplicationSettings

settings = ApplicationSettings(
    server=ServerSettings(max_concurrent_jobs=5),
    processing=ProcessingSettings(default_pipeline="standard")
)
```

### Loading Configuration

```python
from document_parser.config.settings import load_settings, get_settings

# Load from file
settings = load_settings("config.yaml")

# Get singleton
settings = get_settings()
```

## Error Handling

### Exception Hierarchy

```
DocumentParserError (base)
├── ProcessingError
├── ConfigurationError
├── NetworkError
└── ValidationError
```

### Example

```python
from document_parser.core.exceptions import ProcessingError

try:
    result = await processor.process_document("document.pdf")
except ProcessingError as e:
    print(f"Processing failed: {e.message}")
    if e.details:
        print(f"Details: {e.details}")
```
