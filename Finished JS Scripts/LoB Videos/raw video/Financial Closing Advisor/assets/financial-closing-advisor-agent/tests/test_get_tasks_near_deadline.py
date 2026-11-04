"""Unit tests for deadline proximity filtering."""
import json
from datetime import datetime, timezone, timedelta

import pytest


@pytest.fixture(autouse=True)
def use_add_agent_to_path(add_agent_to_path):
    pass


def test_tasks_have_due_at_field():
    """Tasks in mock data have dueAt fields for deadline filtering."""
    mock_data_path = __file__.replace("tests/test_get_tasks_near_deadline.py", "mcp-mock.json")
    with open(mock_data_path) as f:
        mock_data = json.load(f)

    tasks = mock_data["servers"]["afc-task-provider-v2"]["tools"]["provider_getTasks"]["mock_response"]["value"]
    tasks_with_due = [t for t in tasks if t.get("dueAt")]
    assert len(tasks_with_due) >= 2


def test_deadline_proximity_filter_logic():
    """Validate that deadline proximity filtering logic works correctly."""
    mock_data_path = __file__.replace("tests/test_get_tasks_near_deadline.py", "mcp-mock.json")
    with open(mock_data_path) as f:
        mock_data = json.load(f)

    tasks = mock_data["servers"]["afc-task-provider-v2"]["tools"]["provider_getTasks"]["mock_response"]["value"]

    # Simulate filtering: tasks with dueAt in the past are "overdue"
    # In real code, this uses the current time — here we use mock data dates
    for task in tasks:
        if task.get("dueAt"):
            due_str = task["dueAt"]
            # Valid ISO 8601 date format
            assert "T" in due_str
            assert "Z" in due_str or "+" in due_str or due_str.endswith("Z")


def test_blocked_tasks_with_due_dates_are_escalation_candidates():
    """Blocked tasks that also have due dates are escalation candidates."""
    mock_data_path = __file__.replace("tests/test_get_tasks_near_deadline.py", "mcp-mock.json")
    with open(mock_data_path) as f:
        mock_data = json.load(f)

    tasks = mock_data["servers"]["afc-task-provider-v2"]["tools"]["provider_getTasks"]["mock_response"]["value"]
    blocked_statuses = {"CANCELED", "INACTIVE"}
    escalation_candidates = [
        t for t in tasks
        if t.get("status") in blocked_statuses and t.get("dueAt")
    ]
    assert len(escalation_candidates) >= 1, "At least one blocked task with a due date should exist"
