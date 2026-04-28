from __future__ import annotations

import argparse
import json
from pathlib import Path

import pandas as pd

from src.agents import default_agents
from src.metrics import bootstrap_ci, calibration_bins, reason_breakdown, summarize
from src.simulate import generate_dataset


RESULTS_DIR = Path("results")


def run(n_per_regime: int = 3000, seed: int = 42, bootstrap: int = 250, save_raw: bool = False) -> None:
    RESULTS_DIR.mkdir(exist_ok=True)

    config = {"n_per_regime": n_per_regime, "seed": seed, "bootstrap": bootstrap, "save_raw": save_raw}
    (RESULTS_DIR / "run_config.json").write_text(json.dumps(config, indent=2), encoding="utf-8")

    events = generate_dataset(n_per_regime=n_per_regime, seed=seed)
    if save_raw:
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
    if save_raw:
        actions.to_csv(RESULTS_DIR / "actions.csv", index=False)

    summary = summarize(actions)
    summary.to_csv(RESULTS_DIR / "summary.csv", index=False)

    reasons = reason_breakdown(actions)
    reasons.to_csv(RESULTS_DIR / "reason_breakdown.csv", index=False)

    calibration = calibration_bins(actions)
    calibration.to_csv(RESULTS_DIR / "calibration_bins.csv", index=False)

    ci = bootstrap_ci(actions, n_boot=bootstrap, seed=seed + 999)
    ci.to_csv(RESULTS_DIR / "summary_with_ci.csv", index=False)

    print("Saved:")
    for name in ["run_config.json", "summary.csv", "reason_breakdown.csv", "calibration_bins.csv", "summary_with_ci.csv"]:
        print(f"- {RESULTS_DIR / name}")
    if save_raw:
        print(f"- {RESULTS_DIR / 'events.csv'}")
        print(f"- {RESULTS_DIR / 'actions.csv'}")
    print()
    print(summary.to_string(index=False))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run streaming agent safety benchmark.")
    parser.add_argument("--n-per-regime", type=int, default=3000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--bootstrap", type=int, default=250)
    parser.add_argument("--save-raw", action="store_true", help="Save bulky events.csv and actions.csv outputs.")
    args = parser.parse_args()
    run(n_per_regime=args.n_per_regime, seed=args.seed, bootstrap=args.bootstrap, save_raw=args.save_raw)


if __name__ == "__main__":
    main()
