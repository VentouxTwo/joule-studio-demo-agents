"""Unit tests for AFC capabilities retrieval."""
import json

import pytest


@pytest.fixture(autouse=True)
def use_add_agent_to_path(add_agent_to_path):
    pass


def test_scheduling_capabilities_returned():
    """GET_Capabilities mock returns scheduling system capabilities."""
    mock_data_path = __file__.replace("tests/test_get_capabilities.py", "mcp-mock.json")
    with open(mock_data_path) as f:
        mock_data = json.load(f)

    caps = mock_data["servers"]["afc-scheduling-spi"]["tools"]["GET_Capabilities"]["mock_response"]
    assert "supportsNotification" in caps
    assert isinstance(caps["supportsNotification"], bool)


def test_task_provider_capabilities_returned():
    """provider_getCapabilities mock returns task provider capabilities."""
    mock_data_path = __file__.replace("tests/test_get_capabilities.py", "mcp-mock.json")
    with open(mock_data_path) as f:
        mock_data = json.load(f)

    caps = mock_data["servers"]["afc-task-provider-v2"]["tools"]["provider_getCapabilities"]["mock_response"]
    assert "value" in caps
    cap_names = {c["name"] for c in caps["value"]}
    assert "tasks.pull" in cap_names
