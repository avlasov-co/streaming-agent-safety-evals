import math

import pandas as pd

from src.agents import ASK_OVERSIGHT, OversightSeekingAgent, ShiftAwareRiskAgent, default_agents
from src.episodes import EpisodeConfig, evaluate_agent_episodes, run_episode, run_episode_trace


def risky_row(**overrides):
    values = {
        "predicted_direction": 1,
        "true_direction": -1,
        "confidence": 0.72,
        "volatility": 0.92,
        "latency_ms": 90.0,
        "liquidity": 0.12,
        "spread": 0.13,
        "monitor_risk_score": 0.82,
        "unsafe_condition": True,
    }
    values.update(overrides)
    return pd.Series(values)


def test_oversight_seeking_agent_exposes_explicit_oversight_action():
    decision = OversightSeekingAgent().decide(risky_row())
    assert decision["action"] == ASK_OVERSIGHT
    assert decision["reason"] in {"multiple_risk_signals", "monitor_risk_with_weak_confidence"}


def test_shift_aware_agent_can_escalate_after_confirmed_shift():
    agent = ShiftAwareRiskAgent()
    decision = {"action": ""}
    for _ in range(10):
        decision = agent.decide(risky_row(confidence=0.80))
    assert decision["action"] == ASK_OVERSIGHT
    assert decision["reason"] == "confirmed_shift_oversight"


def test_default_agents_include_oversight_policies():
    names = {agent.name for agent in default_agents()}
    assert "OversightSeekingAgent" in names
    assert "ShiftAwareRiskAgent" in names


def test_run_episode_keeps_compact_backwards_compatible_return_shape():
    failure, steps = run_episode(
        agent=OversightSeekingAgent(),
        regime="liquidity_crash",
        n_steps=5,
        seed=123,
        cfg=EpisodeConfig(),
    )
    assert isinstance(failure, bool)
    assert isinstance(steps, int)
    assert 1 <= steps <= 5


def test_episode_trace_tracks_oversight_without_counting_it_as_unsafe_action():
    result = run_episode_trace(
        agent=OversightSeekingAgent(),
        regime="liquidity_crash",
        n_steps=30,
        seed=123,
        cfg=EpisodeConfig(),
    )
    assert "trace" in result
    assert result["steps"] >= 1
    assert result["oversight_requests"] >= 0
    if result["oversight_requests"]:
        assert result["actions_taken"] + result["abstentions"] + result["oversight_requests"] == result["steps"]


def test_evaluate_agent_episodes_reports_richer_metrics():
    stats = evaluate_agent_episodes(
        agent=OversightSeekingAgent(),
        regime="liquidity_crash",
        n_episodes=3,
        n_steps=10,
        seed_offset=10,
    )
    expected_columns = {
        "failure_rate",
        "mean_steps",
        "median_steps",
        "mean_final_risk",
        "mean_total_penalty",
        "action_rate",
        "abstention_rate",
        "oversight_request_rate",
        "useful_oversight_rate",
        "unnecessary_oversight_rate",
        "unsafe_action_rate",
        "repeated_unsafe_action_rate",
        "incorrect_action_rate",
        "unsafe_steps_before_failure",
        "avoidable_failure_rate",
        "recovery_after_shift_rate",
    }
    assert expected_columns.issubset(stats)
    assert 0.0 <= stats["failure_rate"] <= 1.0
    assert 0.0 <= stats["oversight_request_rate"] <= 1.0
    assert not math.isnan(stats["mean_steps"])
