#!/usr/bin/env python3
"""
Example: Basic document parsing usage.

This demonstrates how to use the document processor programmatically.
"""

import asyncio
import logging

from document_parser.config.settings import get_settings
from document_parser.engine.processor import DocumentProcessor


async def main():
    """Main example function."""
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Load configuration
    settings = get_settings()

    # Create processor
    processor = DocumentProcessor(settings)

    # Example 1: Process a local PDF
    logger.info("Example 1: Processing local PDF...")
    try:
        result = await processor.process_document(
            source="sample.pdf",
            pipeline="standard",
        )
        logger.info(f"Processed successfully: {len(result)} characters")
        print(result[:500])  # Print first 500 chars
    except Exception as e:
        logger.error(f"Error: {e}")

    # Example 2: Process from URL
    logger.info("\nExample 2: Processing from URL...")
    try:
        result = await processor.process_document(
            source="https://arxiv.org/pdf/2408.09869",
            pipeline="standard",
        )
        logger.info(f"Processed successfully: {len(result)} characters")
    except Exception as e:
        logger.error(f"Error: {e}")

    # Example 3: Process with custom options
    logger.info("\nExample 3: Processing with custom options...")
    try:
        result = await processor.process_document(
            source="document.pdf",
            pipeline="standard",
            options={
                "ocr_enabled": True,
                "table_accuracy_mode": "accurate",
            },
        )
        logger.info(f"Processed successfully: {len(result)} characters")
    except Exception as e:
        logger.error(f"Error: {e}")


if __name__ == "__main__":
    asyncio.run(main())
