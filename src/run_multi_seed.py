"""
Run the streaming agent safety benchmark across multiple random seeds and
aggregate the results.

This script executes the benchmark for a list of seeds.  For each seed it
generates a synthetic dataset, evaluates the default agents, and collects
summary statistics.  It then computes the mean and standard deviation of
each metric across seeds for every agent–regime pair.  The aggregated
results are written to ``results/multi_seed_summary.csv``.

Example usage::

    python -m src.run_multi_seed --seeds 42 43 44 --n-per-regime 2000

Use this when you want to understand the variability of metrics across
different random draws of the synthetic data.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Iterable, List

import numpy as np
import pandas as pd

from .agents import default_agents
from .metrics import summarize
from .simulate import generate_dataset


RESULTS_DIR = Path("results")


def run_multi_seed(seeds: Iterable[int], n_per_regime: int = 3000) -> pd.DataFrame:
    """Run the benchmark for each seed and aggregate the metrics.

    Args:
        seeds: An iterable of random seeds.
        n_per_regime: Number of events per regime.

    Returns:
        A DataFrame with mean and standard deviation of each metric across seeds.
    """
    all_summaries: List[pd.DataFrame] = []
    for seed in seeds:
        events = generate_dataset(n_per_regime=n_per_regime, seed=seed)
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
        summary = summarize(actions)
        summary["seed"] = seed
        all_summaries.append(summary)

    concatenated = pd.concat(all_summaries, ignore_index=True)
    metrics = [
        "coverage",
        "abstention_rate",
        "accuracy_when_acted",
        "unsafe_action_rate",
        "constraint_violation_rate",
        "false_confident_error_rate",
        "ece_all",
        "ece_when_acted",
        "toy_safety_score",
    ]
    rows = []
    for (agent, regime), group in concatenated.groupby(["agent", "regime"]):
        row = {"agent": agent, "regime": regime}
        for metric in metrics:
            values = group[metric].astype(float).to_numpy()
            finite_values = values[~np.isnan(values)]
            if len(finite_values) == 0:
                row[f"{metric}_mean"] = float("nan")
                row[f"{metric}_std"] = float("nan")
            else:
                row[f"{metric}_mean"] = float(np.mean(finite_values))
                row[f"{metric}_std"] = float(np.std(finite_values, ddof=1)) if len(finite_values) > 1 else float("nan")
        rows.append(row)
    agg = pd.DataFrame(rows)
    return agg.sort_values(["regime", "agent"]).reset_index(drop=True)


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the benchmark across multiple seeds and aggregate results."
    )
    parser.add_argument("--seeds", type=int, nargs="+", default=[1, 2, 3, 4, 5], help="List of seeds to evaluate, e.g. 42 43 44")
    parser.add_argument("--n-per-regime", type=int, default=3000)
    parser.add_argument(
        "--output",
        type=str,
        default=str(RESULTS_DIR / "multi_seed_summary.csv"),
        help="Where to write the aggregated CSV",
    )
    args = parser.parse_args()
    RESULTS_DIR.mkdir(exist_ok=True)
    agg = run_multi_seed(args.seeds, n_per_regime=args.n_per_regime)
    out_path = Path(args.output)
    agg.to_csv(out_path, index=False)
    print(f"Saved multi‑seed summary to {out_path}")
    print()
    print(agg.to_string(index=False))


if __name__ == "__main__":
    main()