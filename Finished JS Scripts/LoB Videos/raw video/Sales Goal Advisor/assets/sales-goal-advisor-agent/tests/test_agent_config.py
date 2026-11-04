"""Tests for agent configuration, system prompt, and instrumentation."""
import pytest
from agent import (
    get_model_name,
    get_temperature,
    get_system_prompt,
    get_summarization_model_name,
    get_circuit_breaker_failure_threshold,
    get_circuit_breaker_cooldown_seconds,
    summarization_trigger_tokens,
)


def test_model_name_is_non_empty():
    model = get_model_name()
    assert isinstance(model, str)
    assert len(model) > 0
    assert "/" in model  # SAP model names use vendor/model format


def test_temperature_is_numeric():
    """Temperature must be a float between 0 and 1."""
    temp = get_temperature()
    assert isinstance(temp, float)
    assert 0.0 <= temp <= 1.0


def test_system_prompt_not_empty():
    prompt = get_system_prompt()
    assert isinstance(prompt, str)
    assert len(prompt) > 100


def test_system_prompt_mentions_successfactors():
    prompt = get_system_prompt().lower()
    assert "successfactors" in prompt or "goals" in prompt


def test_system_prompt_has_confirmation_guard():
    prompt = get_system_prompt()
    assert "NEVER" in prompt or "CRITICAL" in prompt


def test_system_prompt_has_tool_data_instruction():
    prompt = get_system_prompt()
    assert "live data" in prompt.lower() or "tools" in prompt.lower()


def test_system_prompt_has_page_size_guard():
    prompt = get_system_prompt()
    assert "100" in prompt or "pagination" in prompt.lower() or "top" in prompt.lower()


def test_circuit_breaker_threshold_positive():
    assert get_circuit_breaker_failure_threshold() >= 0


def test_circuit_breaker_cooldown_positive():
    assert get_circuit_breaker_cooldown_seconds() > 0


def test_summarization_trigger_positive():
    assert summarization_trigger_tokens() > 0


def test_summarization_model_set():
    model = get_summarization_model_name()
    assert len(model) > 0


def test_agent_response_dataclass():
    from agent import AgentResponse
    r = AgentResponse(status="completed", message="test")
    assert r.status == "completed"
    assert r.message == "test"


def test_agent_response_error_status():
    from agent import AgentResponse
    r = AgentResponse(status="error", message="something went wrong")
    assert r.status == "error"
