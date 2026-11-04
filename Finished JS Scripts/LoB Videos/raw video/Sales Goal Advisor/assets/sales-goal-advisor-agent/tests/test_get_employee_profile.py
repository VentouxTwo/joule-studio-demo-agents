"""Unit test: get_eppublicprofile_for_sfodata MCP tool mock."""
import json
import pytest
from conftest import MOCK_TOOLS


def test_employee_profile_tool_exists():
    """Tool 'get_eppublicprofile_for_sfodata' must be present in mock tools."""
    tool_names = [t.name for t in MOCK_TOOLS]
    assert "get_eppublicprofile_for_sfodata" in tool_names, (
        f"Expected 'get_eppublicprofile_for_sfodata' in tools, got: {tool_names}"
    )


def test_employee_profile_mock_response():
    """Calling the mock tool must return valid employee profile data."""
    tool = next(t for t in MOCK_TOOLS if t.name == "get_eppublicprofile_for_sfodata")
    result = tool.invoke({"userId": "jsmith"})
    data = json.loads(result)
    assert "userId" in data
    assert "fullName" in data
    assert data["userId"] == "jsmith"


def test_employee_profile_has_title():
    """Employee profile mock must include a title field."""
    tool = next(t for t in MOCK_TOOLS if t.name == "get_eppublicprofile_for_sfodata")
    result = json.loads(tool.invoke({"userId": "jsmith"}))
    assert "title" in result
    assert len(result["title"]) > 0
