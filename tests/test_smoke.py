from src.agents import ABSTAIN, RiskGatedAgent, default_agents
from src.metrics import summarize
from src.simulate import generate_dataset


def test_dataset_generation_has_expected_columns():
    df = generate_dataset(n_per_regime=10, seed=1)
    expected = {
        "event_id",
        "regime",
        "true_direction",
        "predicted_direction",
        "confidence",
        "volatility",
        "latency_ms",
        "liquidity",
        "spread",
        "monitor_risk_score",
        "unsafe_condition",
    }
    assert expected.issubset(df.columns)
    assert len(df) > 0


def test_risk_gated_agent_abstains_on_extreme_risk():
    df = generate_dataset(n_per_regime=1, seed=2)
    row = df.iloc[0].copy()
    row["confidence"] = 0.95
    row["volatility"] = 0.99
    row["latency_ms"] = 10
    row["liquidity"] = 0.90
    row["spread"] = 0.01
    decision = RiskGatedAgent().decide(row)
    assert decision["action"] == ABSTAIN
    assert decision["reason"] == "high_volatility"


def test_summary_runs_for_all_agents():
    events = generate_dataset(n_per_regime=5, seed=3)
    rows = []
    for agent in default_agents():
        for _, row in events.iterrows():
            decision = agent.decide(row)
            rows.append({**row.to_dict(), "agent": agent.name, "action": decision["action"], "reason": decision["reason"]})
    import pandas as pd

    summary = summarize(pd.DataFrame(rows))
    assert not summary.empty
    assert "unsafe_action_rate" in summary.columns
