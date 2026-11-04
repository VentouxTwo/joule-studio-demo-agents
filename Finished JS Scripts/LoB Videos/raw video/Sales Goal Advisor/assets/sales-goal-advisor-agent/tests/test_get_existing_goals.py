"""Unit test: list_goal_1_for_sfodata MCP tool mock."""
import json
import pytest
from conftest import MOCK_TOOLS


def test_list_goals_tool_exists():
    """Tool 'list_goal_1_for_sfodata' must be present in mock tools."""
    tool_names = [t.name for t in MOCK_TOOLS]
    assert "list_goal_1_for_sfodata" in tool_names


def test_list_goals_returns_results():
    """Mock must return a list of goals with required fields."""
    tool = next(t for t in MOCK_TOOLS if t.name == "list_goal_1_for_sfodata")
    result = json.loads(tool.invoke({"$filter": "userId eq 'jsmith'", "$top": "10"}))
    assert "results" in result
    assert len(result["results"]) > 0


def test_list_goals_structure():
    """Each goal must have id, name, and category fields."""
    tool = next(t for t in MOCK_TOOLS if t.name == "list_goal_1_for_sfodata")
    goals = json.loads(tool.invoke({}))["results"]
    for goal in goals:
        assert "id" in goal
        assert "name" in goal
        assert "category" in goal


def test_list_goals_covers_three_dimensions():
    """Mock goals must include Pipeline, Activity, and Growth categories."""
    tool = next(t for t in MOCK_TOOLS if t.name == "list_goal_1_for_sfodata")
    goals = json.loads(tool.invoke({}))["results"]
    categories = {g["category"] for g in goals}
    assert "Pipeline" in categories
    assert "Activity" in categories
    assert "Growth" in categories
