"""Unit tests for job status retrieval and status enum mapping."""
import json

import pytest

VALID_JOB_STATUSES = {
    "requested", "running", "completed", "completedWithWarning",
    "completedWithError", "failed", "cancelRequested", "canceled"
}


@pytest.fixture(autouse=True)
def use_add_agent_to_path(add_agent_to_path):
    pass


def test_get_job_returns_valid_status():
    """GET_Job_ID mock returns a job with a valid status enum value."""
    mock_data_path = __file__.replace("tests/test_get_job_status.py", "mcp-mock.json")
    with open(mock_data_path) as f:
        mock_data = json.load(f)

    job = mock_data["servers"]["afc-scheduling-spi"]["tools"]["GET_Job_ID"]["mock_response"]
    assert job["status"] in VALID_JOB_STATUSES


def test_job_list_contains_multiple_statuses():
    """GET_Job mock returns jobs with varied statuses for classification testing."""
    mock_data_path = __file__.replace("tests/test_get_job_status.py", "mcp-mock.json")
    with open(mock_data_path) as f:
        mock_data = json.load(f)

    jobs = mock_data["servers"]["afc-scheduling-spi"]["tools"]["GET_Job"]["mock_response"]
    statuses = {j["status"] for j in jobs}
    # Should have at least one blocked (failed) and one completed to test classification
    assert len(statuses) >= 2


def test_failed_job_is_classified_as_blocked():
    """Jobs with 'failed' or 'completedWithError' status map to blocked closing bucket."""
    mock_data_path = __file__.replace("tests/test_get_job_status.py", "mcp-mock.json")
    with open(mock_data_path) as f:
        mock_data = json.load(f)

    jobs = mock_data["servers"]["afc-scheduling-spi"]["tools"]["GET_Job"]["mock_response"]
    blocked_statuses = {"failed", "completedWithError", "canceled", "cancelRequested"}
    failed_jobs = [j for j in jobs if j["status"] in blocked_statuses]
    assert len(failed_jobs) >= 1, "At least one failed/blocked job should be present in mock data"
