"""
Task queue for managing concurrent job processing.
"""

import asyncio
import logging

from document_parser.processing.job import Job


class TaskQueue:
    """
    Asynchronous task queue for managing document processing jobs.
    """

    def __init__(self, max_size: int = 3):
        """
        Initialize task queue.

        Args:
            max_size: Maximum number of concurrent jobs
        """
        self.max_size = max_size
        self._queue: asyncio.Queue = asyncio.Queue(maxsize=max_size)
        self._logger = logging.getLogger(__name__)

    async def enqueue(self, job: Job) -> bool:
        """
        Add a job to the queue.

        Args:
            job: Job to enqueue

        Returns:
            True if successfully queued, False otherwise
        """
        try:
            # Try to add to queue without blocking
            self._queue.put_nowait(job)
            job.mark_queued()
            self._logger.info(f"Job {job.job_id} enqueued successfully")
            return True

        except asyncio.QueueFull:
            self._logger.warning(f"Queue full, cannot enqueue job {job.job_id}")
            return False

    async def dequeue(self, timeout: float | None = None) -> Job | None:
        """
        Remove and return a job from the queue.

        Args:
            timeout: Maximum time to wait for a job (seconds)

        Returns:
            Job if available, None if timeout
        """
        try:
            if timeout:
                job = await asyncio.wait_for(self._queue.get(), timeout=timeout)
            else:
                job = await self._queue.get()

            job.mark_running()
            self._logger.info(f"Job {job.job_id} dequeued for processing")
            return job

        except asyncio.TimeoutError:
            return None

    def is_full(self) -> bool:
        """
        Check if queue is full.

        Returns:
            True if queue is full
        """
        return self._queue.full()

    def is_empty(self) -> bool:
        """
        Check if queue is empty.

        Returns:
            True if queue is empty
        """
        return self._queue.empty()

    def size(self) -> int:
        """
        Get current queue size.

        Returns:
            Number of jobs in queue
        """
        return self._queue.qsize()

    def get_stats(self) -> dict:
        """
        Get queue statistics.

        Returns:
            Dictionary with queue statistics
        """
        return {
            "current_size": self.size(),
            "max_size": self.max_size,
            "is_full": self.is_full(),
            "is_empty": self.is_empty(),
        }
