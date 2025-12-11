"""
Download manager for remote documents.
"""

import asyncio
import logging
from pathlib import Path
from typing import Optional

import aiofiles
import httpx

from document_parser.config.models import StorageSettings
from document_parser.core.exceptions import NetworkError
from document_parser.utils.file_utils import sanitize_filename, ensure_directory
from document_parser.utils.network_utils import (
    extract_filename_from_url,
    validate_url_scheme,
)


class DownloadManager:
    """
    Manages downloading of remote documents.
    """

    def __init__(self, settings: StorageSettings):
        """
        Initialize download manager.

        Args:
            settings: Storage configuration settings
        """
        self.settings = settings
        self._logger = logging.getLogger(__name__)
        self._temp_dir = Path(settings.temp_directory)

    async def download_file(self, url: str) -> str:
        """
        Download a file from URL to local storage.

        Args:
            url: URL to download from

        Returns:
            Path to downloaded file

        Raises:
            NetworkError: If download fails
        """
        # Validate URL scheme
        if not validate_url_scheme(url, self.settings.allowed_schemes):
            raise NetworkError(
                f"URL scheme not allowed. Allowed schemes: {self.settings.allowed_schemes}",
                details=url,
            )

        # Ensure temp directory exists
        ensure_directory(str(self._temp_dir))

        # Generate filename
        filename = extract_filename_from_url(url) or "downloaded_file"
        safe_filename = sanitize_filename(filename)
        temp_path = self._temp_dir / f"download_{safe_filename}"

        self._logger.info(f"Downloading file from {url}")

        try:
            async with httpx.AsyncClient(
                timeout=httpx.Timeout(self.settings.download_timeout_seconds),
                follow_redirects=True,
            ) as client:
                response = await client.get(url)
                response.raise_for_status()

                # Write file
                async with aiofiles.open(temp_path, "wb") as f:
                    await f.write(response.content)

            self._logger.info(f"Downloaded file to {temp_path}")
            return str(temp_path)

        except httpx.HTTPError as e:
            self._logger.error(f"HTTP error downloading {url}: {e}")
            raise NetworkError(f"Failed to download file from {url}", details=str(e))

        except Exception as e:
            self._logger.error(f"Unexpected error downloading {url}: {e}")
            raise NetworkError(
                f"Unexpected error downloading file from {url}", details=str(e)
            )

    async def cleanup_file(self, file_path: str) -> None:
        """
        Remove a downloaded file.

        Args:
            file_path: Path to file to remove
        """
        try:
            path = Path(file_path)

            # Only remove files in temp directory
            if path.exists() and path.parent == self._temp_dir:
                path.unlink()
                self._logger.debug(f"Cleaned up file: {file_path}")

        except Exception as e:
            self._logger.warning(f"Failed to cleanup file {file_path}: {e}")
