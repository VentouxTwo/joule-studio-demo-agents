"""Unit test: list_goalplantemplate_for_sfodata and default template ID tools."""
import json
import pytest
from conftest import MOCK_TOOLS


def test_list_goal_plan_template_tool_exists():
    tool_names = [t.name for t in MOCK_TOOLS]
    assert "list_goalplantemplate_for_sfodata" in tool_names


def test_list_goal_plan_templates_returns_results():
    tool = next(t for t in MOCK_TOOLS if t.name == "list_goalplantemplate_for_sfodata")
    result = json.loads(tool.invoke({"$top": "5"}))
    assert "results" in result
    assert len(result["results"]) > 0


def test_goal_plan_template_has_name():
    tool = next(t for t in MOCK_TOOLS if t.name == "list_goalplantemplate_for_sfodata")
    templates = json.loads(tool.invoke({}))["results"]
    for t in templates:
        assert "name" in t
        assert "id" in t


def test_default_goal_plan_template_tool_exists():
    tool_names = [t.name for t in MOCK_TOOLS]
    assert "function_getdefaultgoalplantemplateid_for_sfodata" in tool_names


def test_default_goal_plan_template_returns_id():
    tool = next(t for t in MOCK_TOOLS if t.name == "function_getdefaultgoalplantemplateid_for_sfodata")
    result = tool.invoke({})
    # Mock returns the integer 1 (serialized as JSON)
    val = json.loads(result)
    assert isinstance(val, int)
    assert val > 0
