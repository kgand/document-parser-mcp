"""
Factory for creating document processing pipelines.
"""

import logging
from typing import Any, Dict

from document_parser.config.models import ProcessingSettings
from document_parser.processing.job import ProcessingPipeline


class PipelineFactory:
    """
    Factory for creating and configuring document processing pipelines.
    """

    def __init__(self, settings: ProcessingSettings):
        """
        Initialize pipeline factory.

        Args:
            settings: Processing configuration settings
        """
        self.settings = settings
        self._logger = logging.getLogger(__name__)

    def create_standard_pipeline_options(
        self, user_options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create configuration for standard processing pipeline.

        Args:
            user_options: User-provided options

        Returns:
            Pipeline configuration dictionary
        """
        from docling.document_converter import PdfFormatOption
        from docling.datamodel.pipeline_options import PdfPipelineOptions
        from docling.datamodel.base_models import InputFormat

        # Create base pipeline options
        pipeline_opts = PdfPipelineOptions()

        # Configure OCR
        ocr_enabled = user_options.get(
            "ocr_enabled", self.settings.ocr.enable_auto_detect
        )
        pipeline_opts.do_ocr = ocr_enabled

        # Configure enrichments if requested
        if user_options.get("enable_enrichments", False):
            pipeline_opts.do_code_enrichment = True
            pipeline_opts.do_formula_enrichment = True

        # Table extraction mode
        table_mode = user_options.get(
            "table_accuracy_mode", self.settings.pdf.table_accuracy_mode
        )

        # Configure PDF backend
        pdf_backend = user_options.get("pdf_backend", self.settings.pdf.backend)

        self._logger.debug(
            f"Standard pipeline: OCR={ocr_enabled}, backend={pdf_backend}"
        )

        return {
            InputFormat.PDF: PdfFormatOption(pipeline_options=pipeline_opts)
        }

    def create_vlm_pipeline_options(
        self, user_options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create configuration for VLM (Vision-Language Model) pipeline.

        Args:
            user_options: User-provided options

        Returns:
            Pipeline configuration dictionary
        """
        try:
            from docling.document_converter import PdfFormatOption
            from docling.pipeline.vlm_pipeline import VlmPipeline
            from docling.datamodel.pipeline_options import VlmPipelineOptions
            from docling.datamodel import vlm_model_specs
            from docling.datamodel.base_models import InputFormat

            # Choose VLM model based on MLX availability
            if self.settings.performance.enable_mlx_acceleration:
                try:
                    vlm_model = vlm_model_specs.SMOLDOCLING_MLX
                    self._logger.info("Using MLX-accelerated VLM model")
                except AttributeError:
                    vlm_model = vlm_model_specs.SMOLDOCLING_TRANSFORMERS
                    self._logger.info("Using Transformers VLM model")
            else:
                vlm_model = vlm_model_specs.SMOLDOCLING_TRANSFORMERS
                self._logger.info("Using Transformers VLM model")

            pipeline_opts = VlmPipelineOptions(vlm_options=vlm_model)

            return {
                InputFormat.PDF: PdfFormatOption(
                    pipeline_cls=VlmPipeline, pipeline_options=pipeline_opts
                )
            }

        except ImportError as e:
            self._logger.warning(f"VLM pipeline not available: {e}")
            # Fallback to standard pipeline
            return self.create_standard_pipeline_options(user_options)

    def create_asr_pipeline_options(
        self, user_options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create configuration for ASR (Automatic Speech Recognition) pipeline.

        Args:
            user_options: User-provided options

        Returns:
            Pipeline configuration dictionary
        """
        try:
            from docling.document_converter import AudioFormatOption
            from docling.pipeline.asr_pipeline import AsrPipeline
            from docling.datamodel.pipeline_options import AsrPipelineOptions
            from docling.datamodel.base_models import InputFormat

            # Configure ASR model size
            asr_model = user_options.get("asr_model", "whisper_small")

            pipeline_opts = AsrPipelineOptions()

            self._logger.info(f"Using ASR model: {asr_model}")

            return {
                InputFormat.AUDIO: AudioFormatOption(
                    pipeline_cls=AsrPipeline, pipeline_options=pipeline_opts
                )
            }

        except ImportError as e:
            self._logger.warning(f"ASR pipeline not available: {e}")
            # Fallback to standard pipeline
            return self.create_standard_pipeline_options(user_options)

    def create_pipeline_options(
        self, pipeline: ProcessingPipeline, user_options: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create pipeline configuration based on type.

        Args:
            pipeline: Pipeline type
            user_options: User-provided options

        Returns:
            Pipeline configuration dictionary
        """
        if pipeline == ProcessingPipeline.STANDARD:
            return self.create_standard_pipeline_options(user_options)
        elif pipeline == ProcessingPipeline.VLM:
            return self.create_vlm_pipeline_options(user_options)
        elif pipeline == ProcessingPipeline.ASR:
            return self.create_asr_pipeline_options(user_options)
        else:
            # Default to standard
            return self.create_standard_pipeline_options(user_options)

    def get_supported_formats(self) -> Dict[str, Any]:
        """
        Get list of supported input and output formats.

        Returns:
            Dictionary with supported formats
        """
        return {
            "input_formats": [
                "pdf",
                "docx",
                "xlsx",
                "pptx",
                "html",
                "htm",
                "xhtml",
                "md",
                "markdown",
                "csv",
                "png",
                "jpg",
                "jpeg",
                "tiff",
                "tif",
                "bmp",
                "webp",
                "mp3",
                "wav",
                "m4a",
                "flac",
                "xml",
            ],
            "output_formats": ["markdown", "html", "json", "text", "doctags"],
            "pipelines": ["standard", "vlm", "asr"],
        }
