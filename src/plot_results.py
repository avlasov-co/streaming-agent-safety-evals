from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


RESULTS_DIR = Path("results")
FIGURES_DIR = Path("figures")


def _plot_metric(summary: pd.DataFrame, metric: str, title: str, output_name: str, ylabel: str | None = None) -> None:
    pivot = summary.pivot(index="regime", columns="agent", values=metric)
    ax = pivot.plot(kind="bar", figsize=(12, 6))
    ax.set_title(title)
    ax.set_xlabel("Regime")
    ax.set_ylabel(ylabel or metric)
    lower = min(0.0, float(pivot.min().min()) * 1.15)
    upper = max(1.0, float(pivot.max().max()) * 1.15)
    ax.set_ylim(lower, upper)
    ax.legend(title="Agent", fontsize=8)
    plt.xticks(rotation=30, ha="right")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / output_name, dpi=170)
    plt.close()


def _plot_abstention_tradeoff(summary: pd.DataFrame) -> None:
    fig, ax = plt.subplots(figsize=(10, 7))
    for agent, group in summary.groupby("agent"):
        ax.scatter(group["abstention_rate"], group["unsafe_action_rate"], label=agent)
        for _, row in group.iterrows():
            ax.annotate(row["regime"], (row["abstention_rate"], row["unsafe_action_rate"]), fontsize=8)
    ax.set_title("Safety tradeoff: abstention vs unsafe action rate")
    ax.set_xlabel("Abstention rate")
    ax.set_ylabel("Unsafe action rate")
    ax.legend(title="Agent", fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "abstention_tradeoff.png", dpi=170)
    plt.close()


def _plot_reason_breakdown(reasons: pd.DataFrame) -> None:
    abstain_reasons = reasons[~reasons["reason"].isin(["always_act", "confidence_pass", "risk_gate_pass", "monitor_pass", "conservative_pass"])]
    if abstain_reasons.empty:
        return
    top = abstain_reasons.groupby("reason")["count"].sum().sort_values(ascending=False).head(8).index
    subset = abstain_reasons[abstain_reasons["reason"].isin(top)]
    pivot = subset.pivot_table(index="agent", columns="reason", values="count", aggfunc="sum", fill_value=0)
    ax = pivot.plot(kind="bar", stacked=True, figsize=(11, 6))
    ax.set_title("Why agents abstained")
    ax.set_xlabel("Agent")
    ax.set_ylabel("Count")
    ax.legend(title="Reason", fontsize=8)
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "abstention_reasons.png", dpi=170)
    plt.close()



def _plot_calibration(calibration: pd.DataFrame) -> None:
    if calibration.empty:
        return
    fig, ax = plt.subplots(figsize=(8, 6))
    for regime, group in calibration.groupby("regime"):
        group = group[group["count"] > 0]
        if group.empty:
            continue
        ax.plot(group["mean_confidence"], group["empirical_accuracy"], marker="o", label=regime)
    ax.plot([0, 1], [0, 1], linestyle="--", linewidth=1, label="perfect calibration")
    ax.set_title("Calibration by regime")
    ax.set_xlabel("Mean confidence")
    ax.set_ylabel("Empirical accuracy")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.legend(fontsize=8)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / "calibration_by_regime.png", dpi=170)
    plt.close()

def plot_all() -> None:
    FIGURES_DIR.mkdir(exist_ok=True)
    summary_path = RESULTS_DIR / "summary.csv"
    if not summary_path.exists():
        raise FileNotFoundError("Run `python3 -m src.run_eval` first.")

    summary = pd.read_csv(summary_path)
    reasons_path = RESULTS_DIR / "reason_breakdown.csv"
    reasons = pd.read_csv(reasons_path) if reasons_path.exists() else pd.DataFrame()
    calibration_path = RESULTS_DIR / "calibration_bins.csv"
    calibration = pd.read_csv(calibration_path) if calibration_path.exists() else pd.DataFrame()

    _plot_metric(summary, "unsafe_action_rate", "Unsafe action rate by regime", "unsafe_action_rate.png")
    _plot_metric(summary, "false_confident_error_rate", "False confident error rate by regime", "false_confident_error_rate.png")
    _plot_metric(summary, "constraint_violation_rate", "Constraint violation rate by regime", "constraint_violation_rate.png")
    _plot_metric(summary, "toy_safety_score", "Toy safety score by regime", "toy_safety_score.png", ylabel="toy_safety_score")
    _plot_abstention_tradeoff(summary)
    if not reasons.empty:
        _plot_reason_breakdown(reasons)
    if not calibration.empty:
        _plot_calibration(calibration)

    print("Saved figures to figures/")


if __name__ == "__main__":
    plot_all()
