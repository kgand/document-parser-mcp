"""
Task tracker for monitoring job status and history.
"""

import logging
from collections import OrderedDict

from document_parser.processing.job import Job, JobStatus


class TaskTracker:
    """
    Tracks status and history of processing jobs.
    """

    def __init__(self, max_history: int = 100):
        """
        Initialize task tracker.

        Args:
            max_history: Maximum number of jobs to keep in history
        """
        self.max_history = max_history
        self._jobs: dict[str, Job] = OrderedDict()
        self._active_jobs: dict[str, Job] = {}
        self._logger = logging.getLogger(__name__)

    def register_job(self, job: Job) -> None:
        """
        Register a new job for tracking.

        Args:
            job: Job to register
        """
        self._jobs[job.job_id] = job
        self._logger.debug(f"Registered job {job.job_id}")

        # Cleanup old jobs if history limit exceeded
        self._cleanup_history()

    def mark_active(self, job_id: str) -> None:
        """
        Mark a job as actively processing.

        Args:
            job_id: Job identifier
        """
        if job_id in self._jobs:
            job = self._jobs[job_id]
            self._active_jobs[job_id] = job
            self._logger.debug(f"Marked job {job_id} as active")

    def mark_inactive(self, job_id: str) -> None:
        """
        Mark a job as no longer actively processing.

        Args:
            job_id: Job identifier
        """
        if job_id in self._active_jobs:
            del self._active_jobs[job_id]
            self._logger.debug(f"Marked job {job_id} as inactive")

    def get_job(self, job_id: str) -> Job | None:
        """
        Get job by ID.

        Args:
            job_id: Job identifier

        Returns:
            Job if found, None otherwise
        """
        return self._jobs.get(job_id)

    def get_active_jobs(self) -> list[Job]:
        """
        Get all actively processing jobs.

        Returns:
            List of active jobs
        """
        return list(self._active_jobs.values())

    def get_jobs_by_status(self, status: JobStatus) -> list[Job]:
        """
        Get all jobs with a specific status.

        Args:
            status: Job status to filter by

        Returns:
            List of jobs with matching status
        """
        return [job for job in self._jobs.values() if job.status == status]

    def get_recent_jobs(self, limit: int = 10) -> list[Job]:
        """
        Get most recent jobs.

        Args:
            limit: Maximum number of jobs to return

        Returns:
            List of recent jobs
        """
        jobs = list(self._jobs.values())
        return jobs[-limit:]

    def get_statistics(self) -> dict[str, any]:
        """
        Get processing statistics.

        Returns:
            Dictionary with statistics
        """
        total_jobs = len(self._jobs)
        status_counts = {}

        for status in JobStatus:
            count = len(self.get_jobs_by_status(status))
            status_counts[status.value] = count

        completed_jobs = [
            job
            for job in self._jobs.values()
            if job.status == JobStatus.COMPLETED and job.get_duration_seconds()
        ]

        avg_duration = None
        if completed_jobs:
            total_duration = sum(job.get_duration_seconds() for job in completed_jobs)
            avg_duration = total_duration / len(completed_jobs)

        return {
            "total_jobs": total_jobs,
            "active_jobs": len(self._active_jobs),
            "status_counts": status_counts,
            "average_duration_seconds": avg_duration,
        }

    def _cleanup_history(self) -> None:
        """Remove old jobs to maintain history limit."""
        while len(self._jobs) > self.max_history:
            # Remove oldest job (first item in OrderedDict)
            oldest_job_id = next(iter(self._jobs))
            self._jobs.pop(oldest_job_id)
            self._logger.debug(f"Removed old job {oldest_job_id} from history")

    def clear_history(self) -> None:
        """Clear all job history except active jobs."""
        active_job_ids = set(self._active_jobs.keys())
        self._jobs = OrderedDict(
            {
                job_id: job
                for job_id, job in self._jobs.items()
                if job_id in active_job_ids
            }
        )
        self._logger.info("Cleared job history")
