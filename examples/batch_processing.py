#!/usr/bin/env python3
"""
Example: Batch document processing.

This demonstrates how to process multiple documents concurrently.
"""

import asyncio
import logging
from pathlib import Path

from document_parser.config.settings import get_settings
from document_parser.engine.processor import DocumentProcessor


async def process_single_document(
    processor: DocumentProcessor,
    file_path: str,
    output_dir: Path,
) -> None:
    """
    Process a single document and save the result.

    Args:
        processor: Document processor instance
        file_path: Path to input file
        output_dir: Directory for output files
    """
    logger = logging.getLogger(__name__)
    logger.info(f"Processing: {file_path}")

    try:
        # Process document
        result = await processor.process_document(source=file_path)

        # Save result
        output_file = output_dir / f"{Path(file_path).stem}.md"
        output_file.write_text(result, encoding="utf-8")

        logger.info(f"Saved to: {output_file}")

    except Exception as e:
        logger.error(f"Error processing {file_path}: {e}")


async def main():
    """Main batch processing function."""
    # Setup logging
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(__name__)

    # Load configuration
    settings = get_settings()

    # Create processor
    processor = DocumentProcessor(settings)

    # Setup directories
    input_dir = Path("input_documents")
    output_dir = Path("output_markdown")
    output_dir.mkdir(exist_ok=True)

    # Find all supported documents
    patterns = ["*.pdf", "*.docx", "*.pptx"]
    documents = []
    for pattern in patterns:
        documents.extend(input_dir.glob(pattern))

    logger.info(f"Found {len(documents)} documents to process")

    # Process documents concurrently (limited by config)
    max_concurrent = settings.server.max_concurrent_jobs
    for i in range(0, len(documents), max_concurrent):
        batch = documents[i : i + max_concurrent]

        tasks = [
            process_single_document(processor, str(doc), output_dir)
            for doc in batch
        ]

        await asyncio.gather(*tasks)

    logger.info("Batch processing complete!")


if __name__ == "__main__":
    asyncio.run(main())
