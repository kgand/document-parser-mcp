"""
Utility functions for document parser.
"""

from document_parser.utils.file_utils import (
    cleanup_old_files,
    detect_document_type,
    get_file_extension,
    sanitize_filename,
)
from document_parser.utils.logging_utils import (
    get_logger,
    setup_logging,
)
from document_parser.utils.network_utils import (
    extract_filename_from_url,
    is_valid_url,
)
from document_parser.utils.system_utils import (
    generate_unique_id,
    get_available_memory,
    is_mlx_available,
)

__all__ = [
    "sanitize_filename",
    "get_file_extension",
    "detect_document_type",
    "cleanup_old_files",
    "is_valid_url",
    "extract_filename_from_url",
    "setup_logging",
    "get_logger",
    "get_available_memory",
    "is_mlx_available",
    "generate_unique_id",
]
