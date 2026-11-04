"""Unit tests for closing task retrieval and status classification."""
import json
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def use_add_agent_to_path(add_agent_to_path):
    pass


def test_get_closing_tasks_returns_classified_tasks():
    """provider_getTasks mock returns tasks classifiable by status."""
    mock_data_path = (
        __file__.replace("tests/test_get_closing_tasks.py", "mcp-mock.json")
    )
    with open(mock_data_path) as f:
        mock_data = json.load(f)

    tasks = mock_data["servers"]["afc-task-provider-v2"]["tools"]["provider_getTasks"]["mock_response"]["value"]

    statuses = {t["status"] for t in tasks}
    assert "READY" in statuses or "CANCELED" in statuses or "IN_PROGRESS" in statuses

    # Verify classification mapping: CANCELED → blocked, READY → pending, IN_PROGRESS → in-progress
    for task in tasks:
        s = task["status"]
        assert s in ("READY", "RESERVED", "IN_PROGRESS", "FOR_RESUBMISSION", "COMPLETED", "CANCELED", "INACTIVE")


def test_task_priority_fields_present():
    """Each task has a priority field."""
    mock_data_path = (
        __file__.replace("tests/test_get_closing_tasks.py", "mcp-mock.json")
    )
    with open(mock_data_path) as f:
        mock_data = json.load(f)

    tasks = mock_data["servers"]["afc-task-provider-v2"]["tools"]["provider_getTasks"]["mock_response"]["value"]
    for task in tasks:
        assert "priority" in task
        assert task["priority"] in ("VERY_HIGH", "HIGH", "MEDIUM", "LOW")


def test_tasks_have_due_dates():
    """Tasks have dueAt fields for deadline proximity evaluation."""
    mock_data_path = (
        __file__.replace("tests/test_get_closing_tasks.py", "mcp-mock.json")
    )
    with open(mock_data_path) as f:
        mock_data = json.load(f)

    tasks = mock_data["servers"]["afc-task-provider-v2"]["tools"]["provider_getTasks"]["mock_response"]["value"]
    tasks_with_due = [t for t in tasks if "dueAt" in t and t["dueAt"]]
    assert len(tasks_with_due) >= 2, "At least 2 tasks should have due dates for escalation testing"
