"""Unit tests for mcp_providers/agw.py utility functions (no network required)."""
import json
import os
import pytest
from pathlib import Path


def test_set_and_get_user_token():
    """set_user_token/get_user_token must manage per-context token state."""
    from mcp_providers.agw import set_user_token, get_user_token, reset_user_token

    token_var = set_user_token("test-jwt-token")
    assert get_user_token() == "test-jwt-token"
    reset_user_token(token_var)
    # After reset, token is None
    assert get_user_token() is None


def test_get_user_token_returns_none_by_default():
    """get_user_token() must return None when no token is set."""
    from mcp_providers.agw import get_user_token, reset_user_token, set_user_token

    # Ensure clean state
    token_var = set_user_token(None)
    result = get_user_token()
    assert result is None
    reset_user_token(token_var)


def test_reset_user_token():
    """reset_user_token must restore previous token state."""
    from mcp_providers.agw import set_user_token, get_user_token, reset_user_token

    # Set initial
    t1 = set_user_token("first-token")
    assert get_user_token() == "first-token"

    # Set second
    t2 = set_user_token("second-token")
    assert get_user_token() == "second-token"

    # Reset to first
    reset_user_token(t2)
    assert get_user_token() == "first-token"

    # Clean up
    reset_user_token(t1)


def test_build_mock_tools_with_mock_file():
    """_build_mock_tools() must return tools when mcp-mock.json exists."""
    import os
    os.environ["IBD_TESTING"] = "true"

    from mcp_providers.agw import _build_mock_tools

    tools = _build_mock_tools()
    assert isinstance(tools, list)
    # Should have tools since mcp-mock.json exists in the asset root
    assert len(tools) > 0


def test_build_mock_tools_returns_langchain_tools():
    """_build_mock_tools() must return LangChain BaseTool instances."""
    import os
    os.environ["IBD_TESTING"] = "true"

    from mcp_providers.agw import _build_mock_tools
    from langchain_core.tools import BaseTool

    tools = _build_mock_tools()
    for tool in tools:
        assert isinstance(tool, BaseTool)
        assert len(tool.name) > 0


@pytest.mark.asyncio
async def test_get_mcp_tools_ibd_mode_returns_mocks():
    """get_mcp_tools() in IBD_TESTING mode must return mock tools without AGW calls."""
    import os
    os.environ["IBD_TESTING"] = "true"

    from mcp_providers.agw import get_mcp_tools
    tools = await get_mcp_tools()

    assert isinstance(tools, list)
    assert len(tools) > 0
    # Verify tool names match mcp-mock.json
    tool_names = [t.name for t in tools]
    assert "get_eppublicprofile_for_sfodata" in tool_names
    assert "create_goal_1_for_sfodata" in tool_names
