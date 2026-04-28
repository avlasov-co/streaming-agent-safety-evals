"""
Perform threshold sweeps for risk‑aware agents to explore safety–performance trade‑offs.

This script varies the confidence threshold and volatility limits of the
``RiskGatedAgent`` and the monitor limit of the ``MonitorThenActAgent``.  For
each configuration it generates a dataset, runs the agent across all
regimes, summarises metrics, and records coverage and unsafe action rate.
The aggregate results are saved to ``results/threshold_sweep.csv``.  An
optional scatter plot of coverage versus unsafe action rate is saved to
``figures/threshold_sweep.png``.

Use this tool to understand how tuning agent parameters trades off acting
frequently against acting safely.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from .agents import RiskGatedAgent, MonitorThenActAgent
from .metrics import summarize
from .simulate import generate_dataset


RESULTS_DIR = Path("results")
FIGURES_DIR = Path("figures")


def run_sweep(
    confidence_thresholds: List[float],
    volatility_limits: List[float],
    monitor_limits: List[float],
    n_per_regime: int = 3000,
    seed: int = 42,
) -> pd.DataFrame:
    """Run threshold sweeps for ``RiskGatedAgent`` and ``MonitorThenActAgent``.

    Args:
        confidence_thresholds: Values to test for confidence gating.
        volatility_limits: Values to test for volatility gating (RiskGatedAgent).
        monitor_limits: Values to test for monitor gating (MonitorThenActAgent).
        n_per_regime: Number of events per regime.
        seed: Random seed for dataset generation.

    Returns:
        A DataFrame with mean coverage and unsafe action rate for each configuration and agent.
    """
    events = generate_dataset(n_per_regime=n_per_regime, seed=seed)
    results = []

    # Sweep RiskGatedAgent
    for ct in confidence_thresholds:
        for vl in volatility_limits:
            agent = RiskGatedAgent(confidence_threshold=ct, volatility_limit=vl)
            action_rows = []
            for _, row in events.iterrows():
                decision = agent.decide(row)
                action_rows.append({**row.to_dict(), "agent": agent.name, "action": decision["action"], "reason": decision["reason"]})
            summary = summarize(pd.DataFrame(action_rows))
            # Aggregate across regimes by taking means
            mean_cov = float(summary["coverage"].mean())
            mean_unsafe = float(summary["unsafe_action_rate"].mean())
            results.append({
                "agent": agent.name,
                "confidence_threshold": ct,
                "volatility_limit": vl,
                "monitor_limit": np.nan,
                "coverage_mean": mean_cov,
                "unsafe_action_rate_mean": mean_unsafe,
            })

    # Sweep MonitorThenActAgent
    for ct in confidence_thresholds:
        for ml in monitor_limits:
            agent = MonitorThenActAgent(confidence_threshold=ct, monitor_risk_limit=ml)
            action_rows = []
            for _, row in events.iterrows():
                decision = agent.decide(row)
                action_rows.append({**row.to_dict(), "agent": agent.name, "action": decision["action"], "reason": decision["reason"]})
            summary = summarize(pd.DataFrame(action_rows))
            mean_cov = float(summary["coverage"].mean())
            mean_unsafe = float(summary["unsafe_action_rate"].mean())
            results.append({
                "agent": agent.name,
                "confidence_threshold": ct,
                "volatility_limit": np.nan,
                "monitor_limit": ml,
                "coverage_mean": mean_cov,
                "unsafe_action_rate_mean": mean_unsafe,
            })

    return pd.DataFrame(results)


def save_plot(df: pd.DataFrame, out_path: Path) -> None:
    """Create a scatter plot of coverage versus unsafe action rate for the threshold sweep.

    Points are coloured by agent type and annotated with parameter values.

    Args:
        df: DataFrame returned from ``run_sweep``.
        out_path: Destination file path for the PNG figure.
    """
    plt.figure(figsize=(8, 6))
    agents = df["agent"].unique()
    colors = {agents[i]: plt.cm.tab10(i) for i in range(len(agents))}
    for _, row in df.iterrows():
        agent = row["agent"]
        plt.scatter(row["coverage_mean"], row["unsafe_action_rate_mean"], color=colors[agent], label=agent, alpha=0.7)
        label = f"ct={row['confidence_threshold']:.2f}"
        if agent == "RiskGatedAgent":
            label += f", vl={row['volatility_limit']:.2f}"
        else:
            label += f", ml={row['monitor_limit']:.2f}"
        plt.text(row["coverage_mean"] + 0.001, row["unsafe_action_rate_mean"] + 0.001, label, fontsize=7, color=colors[agent])
    plt.xlabel("Coverage (mean across regimes)")
    plt.ylabel("Unsafe action rate (mean across regimes)")
    plt.title("Threshold sweep: coverage vs unsafe action rate")
    handles, labels = plt.gca().get_legend_handles_labels()
    by_label = dict(zip(labels, handles))
    plt.legend(by_label.values(), by_label.keys(), fontsize=8)
    plt.grid(True, linestyle="--", alpha=0.4)
    plt.tight_layout()
    out_path.parent.mkdir(exist_ok=True)
    plt.savefig(out_path)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Run threshold sweeps for risk‑aware agents.")
    parser.add_argument("--n-per-regime", type=int, default=3000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument(
        "--output",
        type=str,
        default=str(RESULTS_DIR / "threshold_sweep.csv"),
        help="Destination CSV file for sweep results",
    )
    parser.add_argument("--no-plot", action="store_true", help="Do not generate the scatter plot.")
    args = parser.parse_args()

    # Define sweep ranges.  The values are deliberately coarse; refine as needed.
    confidence_thresholds = [0.60, 0.68, 0.76]
    volatility_limits = [0.70, 0.78, 0.86]
    monitor_limits = [0.50, 0.58, 0.66]

    sweep_df = run_sweep(
        confidence_thresholds=confidence_thresholds,
        volatility_limits=volatility_limits,
        monitor_limits=monitor_limits,
        n_per_regime=args.n_per_regime,
        seed=args.seed,
    )
    RESULTS_DIR.mkdir(exist_ok=True)
    out_path = Path(args.output)
    sweep_df.to_csv(out_path, index=False)
    print(f"Saved threshold sweep results to {out_path}")
    print()
    print(sweep_df.to_string(index=False))
    if not args.no_plot:
        FIGURES_DIR.mkdir(exist_ok=True)
        plot_path = FIGURES_DIR / "threshold_sweep.png"
        save_plot(sweep_df, plot_path)
        print(f"Saved plot to {plot_path}")


if __name__ == "__main__":
    main()