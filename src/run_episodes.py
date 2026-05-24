"""
Command-line interface to run multi-step episode simulations.

This runner now reports richer oversight-aware episode metrics, including
explicit ASK_OVERSIGHT behavior, useful/unnecessary oversight, repeated unsafe
actions, avoidable failures, total penalty, final risk, and recovery after unsafe conditions.
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd

from .agents import default_agents
from .episodes import EpisodeConfig, evaluate_agent_episodes
from .simulate import REGIMES


RESULTS_DIR = Path("results")


def run(
    n_episodes: int = 50,
    n_steps: int = 100,
    seed_offset: int = 1234,
    risk_budget: float = 1.0,
    incorrect_penalty: float = 0.5,
    unsafe_penalty: float = 0.8,
    oversight_penalty: float = 0.05,
) -> None:
    """Execute episode simulations across all agents and regimes."""
    RESULTS_DIR.mkdir(exist_ok=True)
    cfg = EpisodeConfig(
        risk_budget=risk_budget,
        incorrect_penalty=incorrect_penalty,
        unsafe_penalty=unsafe_penalty,
        oversight_penalty=oversight_penalty,
    )
    rows = []
    for agent in default_agents():
        for regime in REGIMES:
            stats = evaluate_agent_episodes(
                agent=agent,
                regime=regime,
                n_episodes=n_episodes,
                n_steps=n_steps,
                seed_offset=seed_offset,
                cfg=cfg,
            )
            rows.append(
                {
                    "agent": agent.name,
                    "regime": regime,
                    "n_episodes": n_episodes,
                    "n_steps": n_steps,
                    **stats,
                }
            )
    df = pd.DataFrame(rows)
    df.to_csv(RESULTS_DIR / "episode_summary.csv", index=False)
    print(f"Saved {RESULTS_DIR / 'episode_summary.csv'}")
    print(df.to_string(index=False))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run oversight-aware multi-step episode simulations.")
    parser.add_argument("--n-episodes", type=int, default=50)
    parser.add_argument("--n-steps", type=int, default=100)
    parser.add_argument("--seed-offset", type=int, default=1234)
    parser.add_argument("--risk-budget", type=float, default=1.0)
    parser.add_argument("--incorrect-penalty", type=float, default=0.5)
    parser.add_argument("--unsafe-penalty", type=float, default=0.8)
    parser.add_argument("--oversight-penalty", type=float, default=0.05)
    args = parser.parse_args()
    run(
        n_episodes=args.n_episodes,
        n_steps=args.n_steps,
        seed_offset=args.seed_offset,
        risk_budget=args.risk_budget,
        incorrect_penalty=args.incorrect_penalty,
        unsafe_penalty=args.unsafe_penalty,
        oversight_penalty=args.oversight_penalty,
    )


if __name__ == "__main__":
    main()
