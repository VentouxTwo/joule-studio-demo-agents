"""Unit tests for CircuitBreaker."""
import asyncio
import pytest
from circuit_breaker import CircuitBreaker


@pytest.mark.asyncio
async def test_circuit_breaker_allows_by_default():
    cb = CircuitBreaker(failure_threshold=3, cooldown_seconds=1)
    assert await cb.allows("model-a") is True


@pytest.mark.asyncio
async def test_circuit_breaker_opens_after_threshold():
    cb = CircuitBreaker(failure_threshold=3, cooldown_seconds=60)
    for _ in range(3):
        await cb.record_failure("model-a")
    assert await cb.allows("model-a") is False


@pytest.mark.asyncio
async def test_circuit_breaker_resets_on_success():
    cb = CircuitBreaker(failure_threshold=2, cooldown_seconds=60)
    await cb.record_failure("model-a")
    await cb.record_success("model-a")
    # After success, failure count resets — one more failure shouldn't open
    await cb.record_failure("model-a")
    assert await cb.allows("model-a") is True


@pytest.mark.asyncio
async def test_circuit_breaker_different_models_independent():
    cb = CircuitBreaker(failure_threshold=2, cooldown_seconds=60)
    await cb.record_failure("model-a")
    await cb.record_failure("model-a")
    # model-a is open, model-b should still be allowed
    assert await cb.allows("model-a") is False
    assert await cb.allows("model-b") is True


@pytest.mark.asyncio
async def test_circuit_breaker_opens_exactly_at_threshold():
    """Circuit breaker opens after exactly failure_threshold failures."""
    cb = CircuitBreaker(failure_threshold=2, cooldown_seconds=60)
    # One failure below threshold — still allows
    await cb.record_failure("model-x")
    assert await cb.allows("model-x") is True
    # Second failure reaches threshold — now closed
    await cb.record_failure("model-x")
    assert await cb.allows("model-x") is False
