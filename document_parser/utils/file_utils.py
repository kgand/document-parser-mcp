"""
File-related utility functions.
"""

import re
import time
from pathlib import Path
from urllib.parse import urlparse


def sanitize_filename(filename: str) -> str:
    """
    Create a safe filename by removing problematic characters.

    Args:
        filename: Original filename

    Returns:
        Sanitized filename
    """
    # Remove or replace problematic characters
    safe = re.sub(r'[<>:"/\\|?*]', "_", filename)

    # Limit length to avoid filesystem issues
    max_length = 200
    if len(safe) > max_length:
        name_part, ext_part = Path(safe).stem, Path(safe).suffix
        safe = name_part[: max_length - len(ext_part)] + ext_part

    return safe


def get_file_extension(file_path: str) -> str:
    """
    Extract file extension from path or URL.

    Args:
        file_path: File path or URL

    Returns:
        Lowercase file extension with dot (e.g., '.pdf')
    """
    from document_parser.utils.network_utils import is_valid_url

    if is_valid_url(file_path):
        parsed = urlparse(file_path)
        path = parsed.path
    else:
        path = file_path

    return Path(path).suffix.lower()


def detect_document_type(source: str) -> tuple[str, str]:
    """
    Detect document type and suggest optimal processing pipeline.

    Args:
        source: File path or URL

    Returns:
        Tuple of (document_type, suggested_pipeline)
    """
    extension = get_file_extension(source)

    # Extension to type mapping
    type_mapping = {
        ".pdf": "pdf",
        ".docx": "office_document",
        ".xlsx": "office_document",
        ".pptx": "office_document",
        ".html": "web_document",
        ".htm": "web_document",
        ".xhtml": "web_document",
        ".md": "markdown",
        ".markdown": "markdown",
        ".csv": "spreadsheet",
        ".png": "image",
        ".jpg": "image",
        ".jpeg": "image",
        ".tiff": "image",
        ".tif": "image",
        ".bmp": "image",
        ".webp": "image",
        ".mp3": "audio",
        ".wav": "audio",
        ".m4a": "audio",
        ".flac": "audio",
        ".xml": "structured_data",
        ".json": "structured_data",
    }

    # Pipeline suggestions based on type
    pipeline_mapping = {
        "pdf": "standard",
        "office_document": "standard",
        "web_document": "standard",
        "markdown": "standard",
        "spreadsheet": "standard",
        "image": "vlm",  # Images benefit from vision models
        "audio": "asr",  # Audio requires speech recognition
        "structured_data": "standard",
    }

    doc_type = type_mapping.get(extension, "unknown")
    suggested_pipeline = pipeline_mapping.get(doc_type, "standard")

    return doc_type, suggested_pipeline


def cleanup_old_files(directory: str, max_age_hours: int = 24) -> int:
    """
    Remove files older than specified age from a directory.

    Args:
        directory: Directory path to clean
        max_age_hours: Maximum file age in hours

    Returns:
        Number of files removed
    """
    dir_path = Path(directory)
    if not dir_path.exists():
        return 0

    max_age_seconds = max_age_hours * 3600
    current_time = time.time()
    removed_count = 0

    for item in dir_path.iterdir():
        try:
            if item.is_file():
                file_age = current_time - item.stat().st_mtime
                if file_age > max_age_seconds:
                    item.unlink()
                    removed_count += 1
            elif item.is_dir():
                # Remove empty directories
                try:
                    if not any(item.iterdir()):
                        item.rmdir()
                        removed_count += 1
                except OSError:
                    pass
        except Exception:
            # Skip files that can't be accessed
            continue

    return removed_count


def ensure_directory(path: str) -> Path:
    """
    Ensure a directory exists, creating it if necessary.

    Args:
        path: Directory path

    Returns:
        Path object for the directory
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path
