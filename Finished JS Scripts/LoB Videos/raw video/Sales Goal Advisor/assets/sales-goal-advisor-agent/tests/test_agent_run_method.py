"""Tests for agent._run_agent() method and fallback chain."""
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from langchain_core.messages import AIMessage, HumanMessage
from conftest import MOCK_TOOLS


@pytest.mark.asyncio
async def test_run_agent_returns_string(sample_agent):
    """_run_agent() must return a string response."""
    with patch("agent._load_tools", new=AsyncMock(return_value=MOCK_TOOLS)):
        with patch.object(sample_agent, "_invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = {
                "messages": [
                    HumanMessage(content="What goals should I set?"),
                    AIMessage(content="Based on your territory, I recommend: 1. Close pipeline 2. Schedule calls 3. Expand accounts")
                ]
            }
            result = await sample_agent._run_agent("What goals should I set?", "ctx-001")

    assert isinstance(result, str)
    assert len(result) > 0


@pytest.mark.asyncio
async def test_run_agent_includes_milestone_logging(sample_agent, caplog):
    """_run_agent() must emit M1.achieved log."""
    import logging
    with patch("agent._load_tools", new=AsyncMock(return_value=MOCK_TOOLS)):
        with patch.object(sample_agent, "_invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = {
                "messages": [AIMessage(content="Goal recommendations ready")]
            }
            with caplog.at_level(logging.INFO, logger="agent"):
                await sample_agent._run_agent("Set goals", "ctx-002")

    assert any("M1" in r.message or "M5" in r.message for r in caplog.records)


@pytest.mark.asyncio
async def test_run_agent_uses_mcp_tools(sample_agent):
    """_run_agent() must call _get_tools() to load MCP tools."""
    with patch.object(sample_agent, "_get_tools", new_callable=AsyncMock, return_value=[]) as mock_tools:
        with patch.object(sample_agent, "_invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = {"messages": [AIMessage(content="response")]}
            await sample_agent._run_agent("query", "ctx-003")

    mock_tools.assert_called_once()


@pytest.mark.asyncio
async def test_run_agent_handles_no_tools(sample_agent):
    """_run_agent() must handle the case where no MCP tools are available."""
    with patch.object(sample_agent, "_get_tools", new_callable=AsyncMock, return_value=[]):
        with patch.object(sample_agent, "_invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
            mock_invoke.return_value = {"messages": [AIMessage(content="Tools unavailable")]}
            result = await sample_agent._run_agent("query", "ctx-004")

    assert result == "Tools unavailable"


@pytest.mark.asyncio
async def test_agent_create_graph_returns_graph(sample_agent):
    """_create_graph() must return a compiled state graph."""
    from agent import get_system_prompt
    graph = sample_agent._create_graph(sample_agent.llm, MOCK_TOOLS[:2], get_system_prompt())
    assert graph is not None
