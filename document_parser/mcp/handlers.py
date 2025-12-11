"""
MCP tool handlers.
"""

import json
import logging
from typing import Any

import mcp.types as types

from document_parser.config.models import ApplicationSettings
from document_parser.core.exceptions import ProcessingError
from document_parser.engine.processor import DocumentProcessor
from document_parser.processing.job import Job, ProcessingPipeline
from document_parser.processing.task_queue import TaskQueue
from document_parser.processing.task_tracker import TaskTracker
from document_parser.utils.system_utils import generate_unique_id


class ToolHandlers:
    """
    Handlers for MCP tool calls.
    """

    def __init__(
        self,
        settings: ApplicationSettings,
        processor: DocumentProcessor,
        task_queue: TaskQueue,
        task_tracker: TaskTracker,
    ):
        """
        Initialize tool handlers.

        Args:
            settings: Application settings
            processor: Document processor
            task_queue: Task queue
            task_tracker: Task tracker
        """
        self.settings = settings
        self.processor = processor
        self.task_queue = task_queue
        self.task_tracker = task_tracker
        self._logger = logging.getLogger(__name__)

    async def handle_parse_document(
        self, arguments: dict[str, Any]
    ) -> list[types.TextContent]:
        """
        Handle basic document parsing request.

        Args:
            arguments: Tool arguments

        Returns:
            List of TextContent with result
        """
        source = arguments.get("source")
        if not source:
            raise ValueError("Missing required parameter: source")

        pipeline = arguments.get("pipeline", "auto")
        options = arguments.get("options", {})

        self._logger.info(f"Parsing document: {source}")

        try:
            # Create job
            job_id = generate_unique_id("job")
            pipeline_enum = self._parse_pipeline_string(pipeline)

            job = Job(
                job_id=job_id,
                source_path=source,
                pipeline=pipeline_enum,
                options=options,
            )

            # Register and queue job
            self.task_tracker.register_job(job)
            queued = await self.task_queue.enqueue(job)

            if not queued:
                raise ProcessingError("Queue is full, please try again later")

            # Process job
            job = await self.task_queue.dequeue()
            if not job:
                raise ProcessingError("Failed to retrieve job from queue")

            self.task_tracker.mark_active(job.job_id)

            try:
                # Process document
                markdown_result = await self.processor.process_document(
                    job.source_path, job.pipeline.value, job.options
                )

                # Mark completed
                job.mark_completed(markdown_result)
                self.task_tracker.mark_inactive(job.job_id)

                return [types.TextContent(type="text", text=markdown_result)]

            except Exception as e:
                job.mark_failed(str(e))
                self.task_tracker.mark_inactive(job.job_id)
                raise

        except ProcessingError:
            raise

        except Exception as e:
            self._logger.error(f"Error parsing document: {e}")
            raise ProcessingError(f"Document parsing failed: {str(e)}")

    async def handle_parse_document_advanced(
        self, arguments: dict[str, Any]
    ) -> list[types.TextContent]:
        """
        Handle advanced document parsing request.

        Args:
            arguments: Tool arguments

        Returns:
            List of TextContent with result
        """
        source = arguments.get("source")
        if not source:
            raise ValueError("Missing required parameter: source")

        pipeline = arguments.get("pipeline", "standard")

        # Extract advanced options
        options = {
            "ocr_enabled": arguments.get("ocr_enabled"),
            "ocr_language": arguments.get("ocr_language"),
            "table_accuracy_mode": arguments.get("table_accuracy_mode"),
            "pdf_backend": arguments.get("pdf_backend"),
            "enable_enrichments": arguments.get("enable_enrichments", False),
        }

        # Remove None values
        options = {k: v for k, v in options.items() if v is not None}

        self._logger.info(f"Advanced parsing: {source} with pipeline: {pipeline}")

        # Use same logic as basic parsing
        arguments_copy = {
            "source": source,
            "pipeline": pipeline,
            "options": options,
        }

        return await self.handle_parse_document(arguments_copy)

    async def handle_get_job_status(
        self, arguments: dict[str, Any]
    ) -> list[types.TextContent]:
        """
        Handle job status request.

        Args:
            arguments: Tool arguments

        Returns:
            List of TextContent with status
        """
        job_id = arguments.get("job_id")
        if not job_id:
            raise ValueError("Missing required parameter: job_id")

        job = self.task_tracker.get_job(job_id)
        if not job:
            raise ValueError(f"Job not found: {job_id}")

        status_data = job.to_dict()

        return [types.TextContent(type="text", text=json.dumps(status_data, indent=2))]

    async def handle_list_supported_formats(
        self, arguments: dict[str, Any]
    ) -> list[types.TextContent]:
        """
        Handle supported formats request.

        Args:
            arguments: Tool arguments

        Returns:
            List of TextContent with formats
        """
        formats = self.processor.get_supported_formats()

        return [types.TextContent(type="text", text=json.dumps(formats, indent=2))]

    async def handle_get_queue_statistics(
        self, arguments: dict[str, Any]
    ) -> list[types.TextContent]:
        """
        Handle queue statistics request.

        Args:
            arguments: Tool arguments

        Returns:
            List of TextContent with statistics
        """
        queue_stats = self.task_queue.get_stats()
        tracker_stats = self.task_tracker.get_statistics()

        combined_stats = {
            "queue": queue_stats,
            "processing": tracker_stats,
        }

        return [
            types.TextContent(type="text", text=json.dumps(combined_stats, indent=2))
        ]

    def _parse_pipeline_string(self, pipeline: str) -> ProcessingPipeline:
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

        return pipeline_map.get(pipeline.lower(), ProcessingPipeline.AUTO)
