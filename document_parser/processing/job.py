"""
Job model and status definitions.
"""

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional


class JobStatus(Enum):
    """Status of a processing job."""

    PENDING = "pending"
    QUEUED = "queued"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ProcessingPipeline(Enum):
    """Available processing pipelines."""

    STANDARD = "standard"
    VLM = "vlm"
    ASR = "asr"
    AUTO = "auto"


@dataclass
class Job:
    """
    Represents a document processing job.
    """

    job_id: str
    source_path: str
    pipeline: ProcessingPipeline
    options: dict[str, Any] = field(default_factory=dict)
    status: JobStatus = JobStatus.PENDING
    created_at: datetime = field(default_factory=datetime.now)
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    result_data: Optional[str] = None
    error_message: Optional[str] = None
    error_details: Optional[str] = None
    retry_count: int = 0

    def mark_queued(self) -> None:
        """Mark job as queued."""
        self.status = JobStatus.QUEUED

    def mark_running(self) -> None:
        """Mark job as running and record start time."""
        self.status = JobStatus.RUNNING
        self.started_at = datetime.now()

    def mark_completed(self, result: str) -> None:
        """
        Mark job as completed and store result.

        Args:
            result: Processing result data
        """
        self.status = JobStatus.COMPLETED
        self.completed_at = datetime.now()
        self.result_data = result

    def mark_failed(self, error: str, details: Optional[str] = None) -> None:
        """
        Mark job as failed and store error information.

        Args:
            error: Error message
            details: Optional error details
        """
        self.status = JobStatus.FAILED
        self.completed_at = datetime.now()
        self.error_message = error
        self.error_details = details

    def mark_cancelled(self) -> None:
        """Mark job as cancelled."""
        self.status = JobStatus.CANCELLED
        self.completed_at = datetime.now()

    def increment_retry(self) -> None:
        """Increment retry counter."""
        self.retry_count += 1

    def get_duration_seconds(self) -> Optional[float]:
        """
        Get job duration in seconds.

        Returns:
            Duration in seconds, or None if not completed
        """
        if self.started_at and self.completed_at:
            delta = self.completed_at - self.started_at
            return delta.total_seconds()
        return None

    def to_dict(self) -> dict[str, Any]:
        """
        Convert job to dictionary representation.

        Returns:
            Job data as dictionary
        """
        return {
            "job_id": self.job_id,
            "source_path": self.source_path,
            "pipeline": self.pipeline.value,
            "status": self.status.value,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": (
                self.completed_at.isoformat() if self.completed_at else None
            ),
            "duration_seconds": self.get_duration_seconds(),
            "retry_count": self.retry_count,
            "error_message": self.error_message,
        }
