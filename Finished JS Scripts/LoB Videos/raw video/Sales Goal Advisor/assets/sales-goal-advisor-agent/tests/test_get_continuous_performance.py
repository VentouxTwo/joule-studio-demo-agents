"""Unit test: continuous performance management MCP tools (activities, achievements, performance trends)."""
import json
import pytest
from conftest import MOCK_TOOLS


def test_list_activity_tool_exists():
    tool_names = [t.name for t in MOCK_TOOLS]
    assert "list_activity_for_sfodata" in tool_names


def test_list_activity_returns_results():
    tool = next(t for t in MOCK_TOOLS if t.name == "list_activity_for_sfodata")
    result = json.loads(tool.invoke({"$filter": "subjectUserId eq 'jsmith'"}))
    assert "results" in result
    assert len(result["results"]) > 0


def test_list_activity_structure():
    tool = next(t for t in MOCK_TOOLS if t.name == "list_activity_for_sfodata")
    activities = json.loads(tool.invoke({}))["results"]
    for act in activities:
        assert "activityId" in act
        assert "activityName" in act
        assert "subjectUserId" in act


def test_list_achievement_tool_exists():
    tool_names = [t.name for t in MOCK_TOOLS]
    assert "list_achievement_for_sfodata" in tool_names


def test_list_achievement_returns_results():
    tool = next(t for t in MOCK_TOOLS if t.name == "list_achievement_for_sfodata")
    result = json.loads(tool.invoke({}))
    assert "results" in result
    assert len(result["results"]) > 0


def test_performance_trend_tool_exists():
    tool_names = [t.name for t in MOCK_TOOLS]
    assert "list_trenddata_sysoverallperformance_for_sfodata" in tool_names


def test_performance_trend_returns_results():
    tool = next(t for t in MOCK_TOOLS if t.name == "list_trenddata_sysoverallperformance_for_sfodata")
    result = json.loads(tool.invoke({"$filter": "userId eq 'jsmith'"}))
    assert "results" in result
    ratings = [r["rating"] for r in result["results"]]
    assert all(isinstance(r, (int, float)) for r in ratings)
