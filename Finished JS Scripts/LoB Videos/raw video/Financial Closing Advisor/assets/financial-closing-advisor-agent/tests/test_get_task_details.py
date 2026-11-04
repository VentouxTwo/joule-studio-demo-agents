"""Unit tests for single task detail retrieval."""
import json

import pytest


@pytest.fixture(autouse=True)
def use_add_agent_to_path(add_agent_to_path):
    pass


def test_get_task_returns_full_details():
    """provider_getTask mock returns task with all key fields."""
    mock_data_path = __file__.replace("tests/test_get_task_details.py", "mcp-mock.json")
    with open(mock_data_path) as f:
        mock_data = json.load(f)

    task = mock_data["servers"]["afc-task-provider-v2"]["tools"]["provider_getTask"]["mock_response"]

    required_fields = ["urn", "localId", "definitionId", "status", "priority",
                       "createdAt", "modifiedAt", "subject", "recipientUsers"]
    for field in required_fields:
        assert field in task, f"Missing required field: {field}"


def test_task_subject_is_localized():
    """Task subject contains at least one localized entry."""
    mock_data_path = __file__.replace("tests/test_get_task_details.py", "mcp-mock.json")
    with open(mock_data_path) as f:
        mock_data = json.load(f)

    task = mock_data["servers"]["afc-task-provider-v2"]["tools"]["provider_getTask"]["mock_response"]
    assert isinstance(task["subject"], list)
    assert len(task["subject"]) >= 1
    assert "text" in task["subject"][0]


def test_task_has_recipient_users():
    """Task has at least one recipient user for owner lookup."""
    mock_data_path = __file__.replace("tests/test_get_task_details.py", "mcp-mock.json")
    with open(mock_data_path) as f:
        mock_data = json.load(f)

    task = mock_data["servers"]["afc-task-provider-v2"]["tools"]["provider_getTask"]["mock_response"]
    assert len(task["recipientUsers"]) >= 1
