"""Integration test: end-to-end agent invocation with mocked LLM and MCP tools."""
from unittest.mock import AsyncMock, MagicMock, patch

import pytest


@pytest.fixture(autouse=True)
def use_add_agent_to_path(add_agent_to_path):
    pass


@pytest.fixture
def mock_llm_response():
    """Return a canned LLM response simulating closing recommendations."""
    response_content = (
        "Based on the current closing task status, here are my next-action recommendations:\n\n"
        "1. **Asset Depreciation Run (BLOCKED - HIGH priority)** - This task is blocked due to "
        "missing asset master data. Recommended action: Verify asset acquisition dates for "
        "asset class 3000 in company code 1000. This task is blocking the downstream "
        "GL Period Close completion.\n\n"
        "2. **Inventory Valuation (IN-PROGRESS - MEDIUM priority)** - Currently being processed. "
        "Monitor progress and ensure completion before March 29 deadline.\n\n"
        "3. **GL Period Close (PENDING - VERY HIGH priority)** - Cannot start until Asset "
        "Depreciation Run is unblocked. Prioritize fixing the upstream blocker."
    )
    return response_content


@pytest.mark.asyncio
async def test_agent_returns_recommendations(mock_llm_response):
    """Agent returns closing recommendations when queried about next actions."""
    from agent import SampleAgent

    agent = SampleAgent()

    # Mock the LLM to return canned closing recommendations
    mock_ai_message = MagicMock()
    mock_ai_message.content = mock_llm_response

    mock_result = {"messages": [mock_ai_message]}

    with patch.object(agent, "_invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = mock_result

        response = await agent.invoke(
            query="What closing tasks should I action next for the March period close?",
            context_id="test-context-001",
            tools=[],
        )

    assert response.status == "completed"
    assert len(response.message) > 0
    assert any(kw in response.message.lower() for kw in ["recommend", "action", "priorit", "block", "next"])


@pytest.mark.asyncio
async def test_agent_stream_yields_recommendations(mock_llm_response):
    """Agent stream yields a final completed message with recommendations."""
    from agent import SampleAgent

    agent = SampleAgent()

    mock_ai_message = MagicMock()
    mock_ai_message.content = mock_llm_response
    mock_result = {"messages": [mock_ai_message]}

    with patch.object(agent, "_invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = mock_result

        chunks = []
        async for chunk in agent.stream(
            query="What closing tasks are blocked right now?",
            context_id="test-context-002",
            tools=[],
        ):
            chunks.append(chunk)

    assert len(chunks) >= 2  # At least "Processing..." and final response
    final = chunks[-1]
    assert final["is_task_complete"] is True
    assert final["require_user_input"] is False
    assert len(final["content"]) > 0


@pytest.mark.asyncio
async def test_agent_handles_no_tools_gracefully():
    """Agent gracefully handles the case when no MCP tools are available."""
    from agent import SampleAgent

    agent = SampleAgent()

    mock_ai_message = MagicMock()
    mock_ai_message.content = "I currently have no tools available to retrieve live closing data. Please ensure the SAP Advanced Financial Closing connection is configured."
    mock_result = {"messages": [mock_ai_message]}

    with patch.object(agent, "_invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = mock_result

        response = await agent.invoke(
            query="Show me the current closing task status",
            context_id="test-context-003",
            tools=[],
        )

    assert response.status == "completed"
    assert len(response.message) > 0


@pytest.mark.asyncio
async def test_milestone_instrumentation_logged(mock_llm_response, caplog):
    """Business milestone log statements are emitted during agent execution."""
    import logging
    from agent import SampleAgent

    agent = SampleAgent()

    mock_ai_message = MagicMock()
    mock_ai_message.content = mock_llm_response
    mock_result = {"messages": [mock_ai_message]}

    with patch.object(agent, "_invoke_with_fallback", new_callable=AsyncMock) as mock_invoke:
        mock_invoke.return_value = mock_result

        with caplog.at_level(logging.INFO, logger="agent"):
            await agent.invoke(
                query="What should I do next in the closing cycle?",
                context_id="test-context-004",
                tools=[],
            )

    # Verify milestone log entries were emitted
    log_messages = " ".join(caplog.messages)
    # M1 milestone should always fire
    assert "M1." in log_messages
