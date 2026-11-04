"""Unit test: create_goal_1_for_sfodata MCP tool mock."""
import json
import pytest
from conftest import MOCK_TOOLS


def test_create_goal_tool_exists():
    """Tool 'create_goal_1_for_sfodata' must be present in mock tools."""
    tool_names = [t.name for t in MOCK_TOOLS]
    assert "create_goal_1_for_sfodata" in tool_names


def test_create_goal_returns_goal_object():
    """Mock must return a goal object with an id after creation."""
    tool = next(t for t in MOCK_TOOLS if t.name == "create_goal_1_for_sfodata")
    result = json.loads(tool.invoke({
        "userId": "jsmith",
        "name": "Close Q3 pipeline",
        "category": "Pipeline",
        "metric": "Revenue closed",
    }))
    assert "id" in result
    assert result["id"] > 0


def test_create_goal_has_state():
    """Created goal mock must have a state field."""
    tool = next(t for t in MOCK_TOOLS if t.name == "create_goal_1_for_sfodata")
    result = json.loads(tool.invoke({"userId": "jsmith", "name": "New goal"}))
    assert "state" in result


def test_create_goal_not_idempotent_via_mcp():
    """Mock tool must accept any call and always return a valid response (stateless mock)."""
    tool = next(t for t in MOCK_TOOLS if t.name == "create_goal_1_for_sfodata")
    r1 = json.loads(tool.invoke({"userId": "jsmith", "name": "Goal A"}))
    r2 = json.loads(tool.invoke({"userId": "jsmith", "name": "Goal B"}))
    # Both calls should succeed (mock is deterministic)
    assert r1["id"] == r2["id"]  # deterministic mock returns same value
