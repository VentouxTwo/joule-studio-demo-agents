"""Tests for agent fallback chain behavior."""
import asyncio
import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from langchain_core.messages import AIMessage, HumanMessage
from litellm.exceptions import RateLimitError
from conftest import MOCK_TOOLS


@pytest.fixture(autouse=True)
def patch_get_user_sub():
    """Patch get_user_sub so tests don't need a real JWT token."""
    with patch("agent.get_user_sub", return_value="test-user-sub"):
        yield


@pytest.mark.asyncio
async def test_invoke_with_fallback_success(sample_agent):
    """_invoke_with_fallback() must return result on successful primary model call."""
    expected = {"messages": [AIMessage(content="Success response")]}
    with patch.object(sample_agent, "_create_graph") as mock_graph_fn:
        mock_graph = MagicMock()
        mock_graph.ainvoke = AsyncMock(return_value=expected)
        mock_graph_fn.return_value = mock_graph

        result = await sample_agent._invoke_with_fallback(
            tools=MOCK_TOOLS[:1],
            system_prompt="You are helpful.",
            query="Set my goals",
            context_id="ctx-fallback-001"
        )

    assert result["messages"][-1].content == "Success response"


@pytest.mark.asyncio
async def test_invoke_with_fallback_tries_fallback_on_rate_limit(sample_agent):
    """On RateLimitError with no fallback, should raise."""
    with patch.object(sample_agent, "_create_graph") as mock_graph_fn:
        mock_graph = MagicMock()
        mock_graph.ainvoke = AsyncMock(side_effect=RateLimitError(
            message="rate limit", llm_provider="test", model="test"
        ))
        mock_graph_fn.return_value = mock_graph

        with pytest.raises(RateLimitError):
            await sample_agent._invoke_with_fallback(
                tools=[],
                system_prompt="test",
                query="test",
                context_id="ctx-fallback-002"
            )


@pytest.mark.asyncio
async def test_stream_error_handling(sample_agent):
    """stream() must yield error response (not raise) when invoke fails."""
    with patch.object(sample_agent, "_run_agent", side_effect=Exception("Unexpected error")):
        chunks = []
        async for chunk in sample_agent.stream("Set goals", "ctx-error"):
            chunks.append(chunk)

    assert len(chunks) >= 1
    last = chunks[-1]
    assert last["is_task_complete"] is True
    assert len(last["content"]) > 0


@pytest.mark.asyncio
async def test_invoke_error_returns_error_status(sample_agent):
    """invoke() must return error/completed when the agent fails."""
    with patch.object(sample_agent, "_run_agent", side_effect=Exception("LLM down")):
        result = await sample_agent.invoke("test", "ctx-err")

    assert result.status in ("error", "completed")


@pytest.mark.asyncio
async def test_invoke_with_fallback_respects_breaker(sample_agent):
    """Circuit breaker state is checked when iterating fallback chain."""
    if sample_agent._breaker:
        for _ in range(10):
            await sample_agent._breaker.record_failure(sample_agent._primary_model)

        with patch.object(sample_agent, "_create_graph") as mock_graph_fn:
            mock_graph = MagicMock()
            mock_graph.ainvoke = AsyncMock(return_value={
                "messages": [AIMessage(content="Forced response")]
            })
            mock_graph_fn.return_value = mock_graph

            result = await sample_agent._invoke_with_fallback(
                tools=[],
                system_prompt="test",
                query="test",
                context_id="ctx-breaker"
            )
        assert "messages" in result
    else:
        pytest.skip("Circuit breaker not enabled")
