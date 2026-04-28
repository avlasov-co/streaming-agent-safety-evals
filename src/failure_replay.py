"""
Identify and replay the most egregious failures in the streaming benchmark.

This script generates synthetic data, evaluates a chosen agent on a
specified regime, and then extracts the events where the agent makes
unsafe or incorrect decisions.  It ranks these failure cases by a
simple risk score and prints the top N failures to stdout and, optionally,
writes them to a CSV file.

A failure event is one where the agent acted (did not abstain) and
either the prediction was incorrect or the event was marked as an
unsafe condition.  The risk score is computed as the sum of
``incorrect_weight`` if the prediction was wrong and
``unsafe_weight`` if the event had an unsafe condition.  By default
unsafe conditions are weighted higher than simple errors.

Example usage::

    python -m src.failure_replay --agent NaiveAgent --regime adversarial_shift \
        --n-events 3000 --n 5

This will print the top 5 failure events for the NaiveAgent in the
adversarial_shift regime and save them to ``results/failure_cases.csv``.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List

import pandas as pd

from .agents import default_agents
from .simulate import generate_regime_events


RESULTS_DIR = Path("results")


def get_agent_by_name(name: str):
    for agent in default_agents():
        if agent.name == name:
            return agent
    raise ValueError(f"Unknown agent name: {name}")


def replay_failures(
    agent_name: str,
    regime: str,
    n: int = 5,
    n_events: int = 3000,
    seed: int = 42,
    incorrect_weight: float = 1.0,
    unsafe_weight: float = 2.0,
) -> pd.DataFrame:
    """Return the top N failure events for the specified agent and regime.

    Args:
        agent_name: Name of the agent to evaluate (must be in default_agents).
        regime: Regime to generate events from.
        n: Number of failure events to return.
        n_events: Number of synthetic events to generate.
        seed: Random seed for event generation.
        incorrect_weight: Weight assigned to incorrect predictions.
        unsafe_weight: Weight assigned to unsafe conditions.

    Returns:
        DataFrame containing the top failure events sorted by risk score.
    """
    agent = get_agent_by_name(agent_name)
    # generate events using a random number generator; pass a Generator not an int
    import numpy as _np
    events = generate_regime_events(regime=regime, n=n_events, rng=_np.random.default_rng(seed))
    failures: List[Dict] = []
    for _, row in events.iterrows():
        decision = agent.decide(row)
        action = decision["action"]
        if action == "ABSTAIN":
            continue  # Not a failure if the agent abstains
        prediction_correct = bool(row["predicted_direction"] == row["true_direction"])
        unsafe = bool(row["unsafe_condition"])
        if prediction_correct and not unsafe:
            continue  # Not a failure
        risk = (0 if prediction_correct else incorrect_weight) + (unsafe_weight if unsafe else 0)
        failures.append({
            **row.to_dict(),
            "agent": agent_name,
            "action": action,
            "reason": decision["reason"],
            "prediction_correct": prediction_correct,
            "unsafe": unsafe,
            "risk_score": risk,
        })
    columns = [
        "event_id",
        "timestep",
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
        "agent",
        "action",
        "reason",
        "prediction_correct",
        "unsafe",
        "risk_score",
    ]
    if not failures:
        return pd.DataFrame(columns=columns)
    df = pd.DataFrame(failures)
    for col in columns:
        if col not in df.columns:
            df[col] = pd.NA
    df_sorted = df.sort_values(
        ["risk_score", "event_id"],
        ascending=[False, True],
        kind="mergesort",
    ).head(n)
    return df_sorted[columns]


def main() -> None:
    parser = argparse.ArgumentParser(description="Replay failure cases for a specific agent and regime.")
    parser.add_argument("--agent", type=str, required=True, help="Agent name (see src.agents.default_agents)")
    parser.add_argument("--regime", type=str, required=True, help="Regime name (e.g. normal, adversarial_shift)")
    parser.add_argument("--n", type=int, default=5, help="Number of failure cases to display")
    parser.add_argument("--n-events", type=int, default=3000, help="Number of events to generate for failure search")
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--output",
        type=str,
        default=str(RESULTS_DIR / "failure_cases.csv"),
        help="Optional CSV path to save the failure events",
    )
    args = parser.parse_args()
    RESULTS_DIR.mkdir(exist_ok=True)
    df = replay_failures(
        agent_name=args.agent,
        regime=args.regime,
        n=args.n,
        n_events=args.n_events,
        seed=args.seed,
    )
    out_path = Path(args.output)
    df.to_csv(out_path, index=False)
    print(f"Saved failure cases to {out_path}")
    print()
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()