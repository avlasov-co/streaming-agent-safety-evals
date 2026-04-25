from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from src.agents import default_agents
from src.metrics import bootstrap_ci, reason_breakdown, summarize
from src.simulate import generate_dataset


RESULTS_DIR = Path("results")


def run(n_per_regime: int = 3000, seed: int = 42, bootstrap: int = 250) -> None:
    RESULTS_DIR.mkdir(exist_ok=True)

    config = {"n_per_regime": n_per_regime, "seed": seed, "bootstrap": bootstrap}
    (RESULTS_DIR / "run_config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")

    events = generate_dataset(n_per_regime=n_per_regime, seed=seed)
    events.to_csv(RESULTS_DIR / "events.csv", index=False)

    action_rows = []
    for agent in default_agents():
        for _, row in events.iterrows():
            decision = agent.decide(row)
            action_rows.append(
                {
                    **row.to_dict(),
                    "agent": agent.name,
                    "action": decision["action"],
                    "reason": decision["reason"],
                }
            )

    actions = pd.DataFrame(action_rows)
    actions.to_csv(RESULTS_DIR / "actions.csv", index=False)

    summary = summarize(actions)
    summary.to_csv(RESULTS_DIR / "summary.csv", index=False)

    reasons = reason_breakdown(actions)
    reasons.to_csv(RESULTS_DIR / "reason_breakdown.csv", index=False)

    ci = bootstrap_ci(actions, n_boot=bootstrap, seed=seed + 999)
    ci.to_csv(RESULTS_DIR / "summary_with_ci.csv", index=False)

    print("Saved:")
    for name in ["run_config.json", "events.csv", "actions.csv", "summary.csv", "reason_breakdown.csv", "summary_with_ci.csv"]:
        print(f"- {RESULTS_DIR / name}")
    print()
    print(summary.to_string(index=False))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run streaming agent safety benchmark.")
    parser.add_argument("--n-per-regime", type=int, default=3000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--bootstrap", type=int, default=250)
    args = parser.parse_args()
    run(n_per_regime=args.n_per_regime, seed=args.seed, bootstrap=args.bootstrap)


if __name__ == "__main__":
    main()
