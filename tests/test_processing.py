"""
Tests for processing components.
"""

from datetime import datetime

from document_parser.processing.job import Job, JobStatus, ProcessingPipeline
from document_parser.processing.task_tracker import TaskTracker


class TestJob:
    """Test Job model."""

    def test_job_creation(self):
        """Test job creation."""
        job = Job(
            job_id="test-123",
            source_path="/path/to/document.pdf",
            pipeline=ProcessingPipeline.STANDARD,
        )

        assert job.job_id == "test-123"
        assert job.status == JobStatus.PENDING
        assert isinstance(job.created_at, datetime)

    def test_job_status_transitions(self):
        """Test job status transitions."""
        job = Job(
            job_id="test-123",
            source_path="document.pdf",
            pipeline=ProcessingPipeline.STANDARD,
        )

        # Pending -> Running
        job.mark_running()
        assert job.status == JobStatus.RUNNING
        assert job.started_at is not None

        # Running -> Completed
        job.mark_completed("Result content")
        assert job.status == JobStatus.COMPLETED
        assert job.result_data == "Result content"
        assert job.completed_at is not None

    def test_job_failure(self):
        """Test job failure handling."""
        job = Job(
            job_id="test-123",
            source_path="document.pdf",
            pipeline=ProcessingPipeline.STANDARD,
        )

        job.mark_running()
        job.mark_failed("Error message", "Error details")

        assert job.status == JobStatus.FAILED
        assert job.error_message == "Error message"
        assert job.error_details == "Error details"

    def test_job_to_dict(self):
        """Test job serialization."""
        job = Job(
            job_id="test-123",
            source_path="document.pdf",
            pipeline=ProcessingPipeline.STANDARD,
        )

        job_dict = job.to_dict()

        assert job_dict["job_id"] == "test-123"
        assert job_dict["pipeline"] == "standard"
        assert job_dict["status"] == "pending"


class TestTaskTracker:
    """Test TaskTracker."""

    def test_tracker_initialization(self):
        """Test tracker initialization."""
        tracker = TaskTracker(max_history=50)
        assert tracker.max_history == 50

    def test_register_job(self):
        """Test job registration."""
        tracker = TaskTracker()
        job = Job(
            job_id="test-123",
            source_path="document.pdf",
            pipeline=ProcessingPipeline.STANDARD,
        )

        tracker.register_job(job)
        retrieved = tracker.get_job("test-123")

        assert retrieved is not None
        assert retrieved.job_id == "test-123"

    def test_active_job_tracking(self):
        """Test active job tracking."""
        tracker = TaskTracker()
        job = Job(
            job_id="test-123",
            source_path="document.pdf",
            pipeline=ProcessingPipeline.STANDARD,
        )

        tracker.register_job(job)
        tracker.mark_active("test-123")

        active_jobs = tracker.get_active_jobs()
        assert len(active_jobs) == 1
        assert active_jobs[0].job_id == "test-123"

        tracker.mark_inactive("test-123")
        active_jobs = tracker.get_active_jobs()
        assert len(active_jobs) == 0

    def test_get_jobs_by_status(self):
        """Test filtering jobs by status."""
        tracker = TaskTracker()

        job1 = Job(
            job_id="job-1",
            source_path="doc1.pdf",
            pipeline=ProcessingPipeline.STANDARD,
        )
        job2 = Job(
            job_id="job-2",
            source_path="doc2.pdf",
            pipeline=ProcessingPipeline.VLM,
        )

        job1.mark_running()
        job2.mark_completed("Result")

        tracker.register_job(job1)
        tracker.register_job(job2)

        running_jobs = tracker.get_jobs_by_status(JobStatus.RUNNING)
        completed_jobs = tracker.get_jobs_by_status(JobStatus.COMPLETED)

        assert len(running_jobs) == 1
        assert len(completed_jobs) == 1

    def test_statistics(self):
        """Test statistics generation."""
        tracker = TaskTracker()

        job = Job(
            job_id="test-123",
            source_path="document.pdf",
            pipeline=ProcessingPipeline.STANDARD,
        )

        tracker.register_job(job)
        stats = tracker.get_statistics()

        assert stats["total_jobs"] == 1
        assert "status_counts" in stats
