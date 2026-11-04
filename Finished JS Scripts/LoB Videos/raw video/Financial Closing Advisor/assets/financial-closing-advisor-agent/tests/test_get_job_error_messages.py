"""Unit tests for job error message retrieval and severity filtering."""
import json

import pytest

VALID_SEVERITIES = {"success", "info", "warning", "error"}


@pytest.fixture(autouse=True)
def use_add_agent_to_path(add_agent_to_path):
    pass


def test_job_result_messages_returned():
    """GET_JobResult_ID_messages mock returns a list of messages."""
    mock_data_path = __file__.replace("tests/test_get_job_error_messages.py", "mcp-mock.json")
    with open(mock_data_path) as f:
        mock_data = json.load(f)

    messages = mock_data["servers"]["afc-scheduling-spi"]["tools"]["GET_JobResult_ID_messages"]["mock_response"]
    assert isinstance(messages, list)
    assert len(messages) >= 1


def test_error_message_has_valid_severity():
    """Each message has a valid severity enum value."""
    mock_data_path = __file__.replace("tests/test_get_job_error_messages.py", "mcp-mock.json")
    with open(mock_data_path) as f:
        mock_data = json.load(f)

    messages = mock_data["servers"]["afc-scheduling-spi"]["tools"]["GET_JobResult_ID_messages"]["mock_response"]
    for msg in messages:
        assert msg["severity"] in VALID_SEVERITIES


def test_error_message_contains_error_text():
    """Error messages contain a human-readable text field."""
    mock_data_path = __file__.replace("tests/test_get_job_error_messages.py", "mcp-mock.json")
    with open(mock_data_path) as f:
        mock_data = json.load(f)

    messages = mock_data["servers"]["afc-scheduling-spi"]["tools"]["GET_JobResult_ID_messages"]["mock_response"]
    error_messages = [m for m in messages if m["severity"] == "error"]
    assert len(error_messages) >= 1
    for msg in error_messages:
        assert "text" in msg
        assert len(msg["text"]) > 0


def test_root_cause_category_detectable():
    """Error message text contains enough context for root cause classification."""
    mock_data_path = __file__.replace("tests/test_get_job_error_messages.py", "mcp-mock.json")
    with open(mock_data_path) as f:
        mock_data = json.load(f)

    messages = mock_data["servers"]["afc-scheduling-spi"]["tools"]["GET_JobResult_ID_messages"]["mock_response"]
    error_messages = [m for m in messages if m["severity"] == "error"]
    # Should have an error that indicates data issue for root cause classification
    data_error_keywords = ["missing", "incomplete", "invalid", "not found"]
    found_data_error = any(
        any(kw in msg["text"].lower() for kw in data_error_keywords)
        for msg in error_messages
    )
    assert found_data_error, "Mock data should contain at least one Data Error type message"
