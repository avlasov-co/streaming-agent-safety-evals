from __future__ import annotations

from pathlib import Path

import pandas as pd


RESULTS_DIR = Path("results")
DOCS_DIR = Path("docs")


def _md_table(df: pd.DataFrame, max_rows: int = 30) -> str:
    shown = df.head(max_rows).copy()
    return shown.to_markdown(index=False)


def generate_report() -> None:
    summary_path = RESULTS_DIR / "summary.csv"
    ci_path = RESULTS_DIR / "summary_with_ci.csv"
    reasons_path = RESULTS_DIR / "reason_breakdown.csv"
    if not summary_path.exists():
        raise FileNotFoundError("Run `python3 -m src.run_eval` first.")

    summary = pd.read_csv(summary_path)
    ci = pd.read_csv(ci_path) if ci_path.exists() else pd.DataFrame()
    reasons = pd.read_csv(reasons_path) if reasons_path.exists() else pd.DataFrame()

    best_by_regime = (
        summary.sort_values(["regime", "toy_safety_score"], ascending=[True, False])
        .groupby("regime")
        .head(1)[["regime", "agent", "toy_safety_score", "unsafe_action_rate", "abstention_rate", "false_confident_error_rate"]]
    )

    naive = summary[summary["agent"] == "NaiveAgent"]
    risk = summary[summary["agent"] == "RiskGatedAgent"]
    merged = naive.merge(risk, on="regime", suffixes=("_naive", "_risk_gated"))
    merged["unsafe_action_reduction"] = merged["unsafe_action_rate_naive"] - merged["unsafe_action_rate_risk_gated"]
    merged["false_confident_error_reduction"] = merged["false_confident_error_rate_naive"] - merged["false_confident_error_rate_risk_gated"]

    report = f"""# Experimental Report

## Summary

This report summarizes a no-training benchmark for evaluating agentic decision behavior under distribution shift. The benchmark compares simple agents that either always act, abstain under low confidence, or use risk/monitoring gates before acting.

The main finding is expected and safety-relevant: agents that always act maintain high coverage but show worse unsafe-action behavior under shifted regimes. Agents with abstention or monitoring reduce unsafe actions, but pay for it with lower coverage.

## Full summary table

{_md_table(summary.round(4), max_rows=100)}

## Best agent by regime according to toy safety score

{_md_table(best_by_regime.round(4), max_rows=20)}

## Risk gate comparison against naive agent

{_md_table(merged[["regime", "unsafe_action_reduction", "false_confident_error_reduction", "abstention_rate_naive", "abstention_rate_risk_gated"]].round(4), max_rows=20)}

## Interpretation

The benchmark is intentionally small. It is not meant to prove that simple gates solve agent safety. It demonstrates a general evaluation pattern:

1. Create deployment regimes that differ from normal evaluation conditions.
2. Measure not only task success, but unsafe behavior and overconfident errors.
3. Compare policies that act aggressively against policies that abstain or defer under risk.
4. Report the tradeoff between useful coverage and safety.

## Limitations

- The environment is synthetic.
- The agents are simple rule-based policies.
- The toy safety score is illustrative, not universal.
- The benchmark does not include strong LLM agents yet.

## Fellowship-scale extension

A stronger version would replace rule-based agents with LLM/tool-using agents, add richer sequential tasks, introduce stronger monitor models, and test whether static evaluation performance predicts dynamic deployment failures.
"""

    if not ci.empty:
        report += "\n## Bootstrap confidence intervals\n\n"
        report += _md_table(ci.round(4), max_rows=200)
        report += "\n"

    if not reasons.empty:
        report += "\n## Decision reason breakdown\n\n"
        report += _md_table(reasons.round(4), max_rows=100)
        report += "\n"

    DOCS_DIR.mkdir(exist_ok=True)
    output = DOCS_DIR / "experimental_report.md"
    output.write_text(report, encoding="utf-8")
    print(f"Saved {output}")


if __name__ == "__main__":
    generate_report()
