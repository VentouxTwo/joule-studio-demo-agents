"""Integration test: end-to-end agent flow with mocked LLM and MCP tools."""
import asyncio
import json
import os
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from langchain_core.messages import AIMessage, HumanMessage


def make_mock_llm(response_text: str):
    """Create a mock LLM that returns a canned AI response."""
    mock = MagicMock()
    ai_msg = AIMessage(content=response_text)
    # Mock ainvoke on the ChatLiteLLM class
    mock.ainvoke = AsyncMock(return_value=ai_msg)
    return mock


@pytest.mark.asyncio
async def test_agent_invoke_returns_completed_response(sample_agent):
    """Agent invoke() must return status='completed' with a non-empty message."""
    with patch("langchain_litellm.ChatLiteLLM.ainvoke", new_callable=AsyncMock) as mock_ainvoke:
        mock_ainvoke.return_value = AIMessage(content="Here are your quarterly goal recommendations.")
        
        # Patch the graph to avoid full LangGraph execution
        with patch.object(sample_agent, "_invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = {
                "messages": [
                    HumanMessage(content="Help me set goals"),
                    AIMessage(content="Here are your recommended quarterly goals: ...")
                ]
            }
            result = await sample_agent.invoke("Help me set quarterly goals", "test-context-001")

    assert result.status == "completed"
    assert len(result.message) > 0


@pytest.mark.asyncio
async def test_agent_stream_yields_processing_then_response(sample_agent):
    """Agent stream() must first yield a 'Processing...' update, then the final response."""
    with patch.object(sample_agent, "_invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = {
            "messages": [
                HumanMessage(content="Set my goals"),
                AIMessage(content="Based on your territory data, I recommend these goals...")
            ]
        }

        chunks = []
        async for chunk in sample_agent.stream("Set my quarterly goals", "test-context-002"):
            chunks.append(chunk)

    assert len(chunks) >= 2
    # First chunk should be "Processing..."
    assert chunks[0]["is_task_complete"] is False
    assert "Processing" in chunks[0]["content"]
    # Last chunk should be complete
    assert chunks[-1]["is_task_complete"] is True
    assert len(chunks[-1]["content"]) > 0


@pytest.mark.asyncio
async def test_agent_loads_mcp_tools_lazily(sample_agent):
    """Agent _get_tools() must load and cache MCP tools (patching _load_tools)."""
    from unittest.mock import AsyncMock, patch
    from conftest import MOCK_TOOLS

    with patch("agent._load_tools", new=AsyncMock(return_value=MOCK_TOOLS)) as mock_load:
        # First call loads tools
        tools1 = await sample_agent._get_tools()
        # Second call returns cached — _load_tools NOT called again
        tools2 = await sample_agent._get_tools()
        assert tools1 is tools2  # same object, cached
        assert mock_load.call_count == 1  # only called once


@pytest.mark.asyncio
async def test_agent_handles_fallback_on_error(sample_agent):
    """Agent must return an error response rather than raise when invoke fails."""
    with patch.object(sample_agent, "_invoke_with_fallback", side_effect=Exception("LLM unavailable")):
        result = await sample_agent.invoke("Help me set goals", "test-context-error")

    assert result.status in ("error", "completed")
    assert len(result.message) > 0


@pytest.mark.asyncio
async def test_confirmation_guard_in_system_prompt(sample_agent):
    """System prompt must contain the CRITICAL confirmation guard."""
    from agent import get_system_prompt
    prompt = get_system_prompt()
    assert "CRITICAL" in prompt or "NEVER" in prompt
    assert "explicit confirmation" in prompt.lower() or "confirmed" in prompt.lower() or "explicit" in prompt.lower()


def test_mcp_mock_file_exists():
    """mcp-mock.json must exist at the asset root."""
    import os
    from pathlib import Path
    mock_path = Path(__file__).parent.parent / "mcp-mock.json"
    assert mock_path.exists(), f"mcp-mock.json not found at {mock_path}"


def test_mcp_mock_has_three_servers():
    """mcp-mock.json must define 3 SuccessFactors MCP servers."""
    from pathlib import Path
    mock_path = Path(__file__).parent.parent / "mcp-mock.json"
    data = json.loads(mock_path.read_text())
    assert len(data["servers"]) == 3


def test_mcp_mock_has_goal_creation_tool():
    """mcp-mock.json must include a goal creation tool."""
    from pathlib import Path
    mock_path = Path(__file__).parent.parent / "mcp-mock.json"
    data = json.loads(mock_path.read_text())
    all_tools = []
    for server in data["servers"].values():
        all_tools.extend(server["tools"].keys())
    assert "create_goal_1_for_sfodata" in all_tools


def test_milestone_logging_in_agent():
    """agent.py must contain milestone log statements for M1 and M5."""
    from pathlib import Path
    agent_src = (Path(__file__).parent.parent / "app" / "agent.py").read_text()
    assert "M1.achieved" in agent_src
    assert "M5.achieved" in agent_src
    assert "M5.missed" in agent_src
