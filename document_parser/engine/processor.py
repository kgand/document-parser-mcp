"""
Main document processor.
"""

import asyncio
import logging
from pathlib import Path
from typing import Any, Dict, Optional

from document_parser.config.models import ApplicationSettings
from document_parser.core.exceptions import ProcessingError
from document_parser.engine.download_manager import DownloadManager
from document_parser.engine.pipeline_factory import PipelineFactory
from document_parser.processing.job import ProcessingPipeline
from document_parser.utils.file_utils import detect_document_type
from document_parser.utils.network_utils import is_valid_url


class DocumentProcessor:
    """
    Main document processing engine using Docling.
    """

    def __init__(self, settings: ApplicationSettings):
        """
        Initialize document processor.

        Args:
            settings: Application configuration settings
        """
        self.settings = settings
        self._logger = logging.getLogger(__name__)
        self.download_manager = DownloadManager(settings.storage)
        self.pipeline_factory = PipelineFactory(settings.processing)

        # Check Docling availability
        self._verify_dependencies()

    def _verify_dependencies(self) -> None:
        """Verify that Docling is available."""
        try:
            import docling

            self._logger.info(f"Docling version: {docling.__version__}")
        except ImportError:
            raise ProcessingError(
                "Docling library not installed",
                details="Install with: pip install docling",
            )

        # Check MLX if enabled
        if self.settings.processing.performance.enable_mlx_acceleration:
            try:
                import mlx

                self._logger.info("MLX acceleration available")
            except ImportError:
                self._logger.warning("MLX not available, using CPU/GPU fallback")

    async def process_document(
        self,
        source: str,
        pipeline: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> str:
        """
        Process a document and convert to markdown.

        Args:
            source: File path or URL to document
            pipeline: Processing pipeline to use (None for auto-detect)
            options: Additional processing options

        Returns:
            Markdown content

        Raises:
            ProcessingError: If processing fails
        """
        options = options or {}
        local_path = None
        is_remote = is_valid_url(source)

        try:
            # Download if URL
            if is_remote:
                local_path = await self.download_manager.download_file(source)
                processing_path = local_path
            else:
                # Verify local file exists
                if not Path(source).exists():
                    raise ProcessingError(f"File not found: {source}")
                processing_path = source

            # Auto-detect pipeline if not specified
            if not pipeline and self.settings.processing.enable_pipeline_auto_detect:
                _, suggested_pipeline = detect_document_type(processing_path)
                pipeline = suggested_pipeline
                self._logger.info(f"Auto-detected pipeline: {pipeline}")

            # Use default pipeline if still not set
            if not pipeline:
                pipeline = self.settings.processing.default_pipeline

            # Convert pipeline string to enum
            pipeline_enum = self._parse_pipeline(pipeline)

            # Process document
            markdown_content = await self._execute_processing(
                processing_path, pipeline_enum, options
            )

            return markdown_content

        except ProcessingError:
            raise

        except Exception as e:
            self._logger.error(f"Unexpected error processing {source}: {e}")
            raise ProcessingError(
                f"Failed to process document: {source}", details=str(e)
            )

        finally:
            # Cleanup downloaded file
            if is_remote and local_path:
                await self.download_manager.cleanup_file(local_path)

    async def _execute_processing(
        self,
        file_path: str,
        pipeline: ProcessingPipeline,
        options: Dict[str, Any],
    ) -> str:
        """
        Execute document processing with specified pipeline.

        Args:
            file_path: Path to file to process
            pipeline: Processing pipeline
            options: Processing options

        Returns:
            Markdown content

        Raises:
            ProcessingError: If processing fails
        """
        self._logger.info(f"Processing {file_path} with {pipeline.value} pipeline")

        try:
            # Run in thread pool to avoid blocking
            loop = asyncio.get_event_loop()
            result = await loop.run_in_executor(
                None, self._process_sync, file_path, pipeline, options
            )

            return result

        except Exception as e:
            # Try fallback if enabled
            if self.settings.retry.enable_pipeline_fallback:
                self._logger.warning(f"Primary processing failed, trying fallback: {e}")
                fallback_result = await self._try_fallback(file_path, pipeline, options)

                if fallback_result:
                    return fallback_result

            raise ProcessingError(
                f"Document processing failed for {file_path}", details=str(e)
            )

    def _process_sync(
        self,
        file_path: str,
        pipeline: ProcessingPipeline,
        options: Dict[str, Any],
    ) -> str:
        """
        Synchronous document processing (runs in thread pool).

        Args:
            file_path: Path to file
            pipeline: Processing pipeline
            options: Processing options

        Returns:
            Markdown content
        """
        from docling.document_converter import DocumentConverter

        # Get pipeline configuration
        pipeline_options = self.pipeline_factory.create_pipeline_options(
            pipeline, options
        )

        # Create converter
        converter = DocumentConverter(format_options=pipeline_options)

        # Convert document
        result = converter.convert(file_path)
        document = result.document

        # Export to markdown
        markdown_content = document.export_to_markdown()

        self._logger.info(
            f"Processing complete: {len(markdown_content)} characters"
        )

        return markdown_content

    async def _try_fallback(
        self,
        file_path: str,
        original_pipeline: ProcessingPipeline,
        options: Dict[str, Any],
    ) -> Optional[str]:
        """
        Try fallback processing strategies.

        Args:
            file_path: Path to file
            original_pipeline: Original pipeline that failed
            options: Processing options

        Returns:
            Markdown content if successful, None otherwise
        """
        fallback_strategies = []

        # Define fallback strategies based on original pipeline
        if original_pipeline == ProcessingPipeline.VLM:
            fallback_strategies.append(ProcessingPipeline.STANDARD)
        elif original_pipeline == ProcessingPipeline.STANDARD:
            # Try with different backend
            if self.settings.retry.enable_backend_fallback:
                fallback_options = options.copy()
                fallback_options["pdf_backend"] = self.settings.processing.pdf.fallback_backend
                fallback_strategies.append(ProcessingPipeline.STANDARD)

        # Try each fallback
        for fallback_pipeline in fallback_strategies:
            try:
                self._logger.info(f"Trying fallback: {fallback_pipeline.value}")
                loop = asyncio.get_event_loop()
                result = await loop.run_in_executor(
                    None, self._process_sync, file_path, fallback_pipeline, options
                )
                self._logger.info("Fallback processing succeeded")
                return result

            except Exception as e:
                self._logger.warning(f"Fallback {fallback_pipeline.value} failed: {e}")
                continue

        return None

    def _parse_pipeline(self, pipeline: str) -> ProcessingPipeline:
        """
        Parse pipeline string to enum.

        Args:
            pipeline: Pipeline name

        Returns:
            ProcessingPipeline enum
        """
        pipeline_map = {
            "standard": ProcessingPipeline.STANDARD,
            "vlm": ProcessingPipeline.VLM,
            "asr": ProcessingPipeline.ASR,
            "auto": ProcessingPipeline.AUTO,
        }

        return pipeline_map.get(
            pipeline.lower(), ProcessingPipeline.STANDARD
        )

    def get_supported_formats(self) -> Dict[str, Any]:
        """
        Get supported document formats.

        Returns:
            Dictionary with supported formats
        """
        return self.pipeline_factory.get_supported_formats()
