"""
MCP tool definitions.
"""

import mcp.types as types
from typing import List


def get_tool_definitions() -> List[types.Tool]:
    """
    Get MCP tool definitions.

    Returns:
        List of Tool definitions
    """
    return [
        types.Tool(
            name="parse_document",
            description="Parse and convert any document (PDF, DOCX, images, audio, etc.) to Markdown format",
            inputSchema={
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string",
                        "description": "File path or URL to the document",
                    },
                    "pipeline": {
                        "type": "string",
                        "enum": ["standard", "vlm", "asr", "auto"],
                        "description": "Processing pipeline (optional, auto-detected if not specified)",
                    },
                    "options": {
                        "type": "object",
                        "description": "Additional processing options",
                        "properties": {
                            "ocr_enabled": {
                                "type": "boolean",
                                "description": "Enable OCR for scanned documents",
                            },
                            "ocr_language": {
                                "type": "string",
                                "description": "OCR language code (e.g., 'eng', 'spa')",
                            },
                            "table_accuracy_mode": {
                                "type": "string",
                                "enum": ["fast", "accurate"],
                                "description": "Table extraction accuracy",
                            },
                            "pdf_backend": {
                                "type": "string",
                                "enum": ["dlparse_v4", "pypdfium2"],
                                "description": "PDF processing backend",
                            },
                            "enable_enrichments": {
                                "type": "boolean",
                                "description": "Enable code/formula enrichments",
                            },
                        },
                    },
                },
                "required": ["source"],
            },
        ),
        types.Tool(
            name="parse_document_advanced",
            description="Advanced document parsing with detailed configuration options",
            inputSchema={
                "type": "object",
                "properties": {
                    "source": {
                        "type": "string",
                        "description": "File path or URL to the document",
                    },
                    "pipeline": {
                        "type": "string",
                        "enum": ["standard", "vlm", "asr"],
                        "description": "Processing pipeline",
                    },
                    "ocr_enabled": {
                        "type": "boolean",
                        "description": "Enable/disable OCR",
                    },
                    "ocr_language": {
                        "type": "string",
                        "description": "OCR language code (e.g., 'eng,spa')",
                    },
                    "table_accuracy_mode": {
                        "type": "string",
                        "enum": ["fast", "accurate"],
                        "description": "Table extraction mode",
                    },
                    "pdf_backend": {
                        "type": "string",
                        "enum": ["dlparse_v4", "pypdfium2"],
                        "description": "PDF backend to use",
                    },
                    "enable_enrichments": {
                        "type": "boolean",
                        "description": "Enable enrichments",
                    },
                },
                "required": ["source"],
            },
        ),
        types.Tool(
            name="get_job_status",
            description="Get the status of a processing job",
            inputSchema={
                "type": "object",
                "properties": {
                    "job_id": {
                        "type": "string",
                        "description": "Job identifier",
                    }
                },
                "required": ["job_id"],
            },
        ),
        types.Tool(
            name="list_supported_formats",
            description="List all supported input formats and processing pipelines",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        ),
        types.Tool(
            name="get_queue_statistics",
            description="Get current queue status and processing statistics",
            inputSchema={
                "type": "object",
                "properties": {},
                "additionalProperties": False,
            },
        ),
    ]
