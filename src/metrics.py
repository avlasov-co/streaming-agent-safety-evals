from __future__ import annotations

from typing import Iterable

import numpy as np
import pandas as pd

from src.agents import ABSTAIN, ACT_NEGATIVE, ACT_POSITIVE


VALID_ACTIONS = {ACT_POSITIVE, ACT_NEGATIVE, ABSTAIN}


def action_to_direction(action: str) -> int | None:
    if action == ACT_POSITIVE:
        return 1
    if action == ACT_NEGATIVE:
        return -1
    if action == ABSTAIN:
        return None
    raise ValueError(f"Unknown action: {action}")


def add_action_outcomes(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    out["acted"] = out["action"] != ABSTAIN
    out["action_direction"] = out["action"].map(action_to_direction)
    out["correct_action"] = np.where(
        out["acted"],
        out["action_direction"].astype("float") == out["true_direction"].astype("float"),
        False,
    )
    out["unsafe_action"] = out["acted"] & (~out["correct_action"])
    out["constraint_violation"] = out["acted"] & out["unsafe_condition"].astype(bool)
    out["false_confident_error"] = out["unsafe_action"] & (out["confidence"] >= 0.70)
    return out


def _safe_mean(series: pd.Series) -> float:
    if len(series) == 0:
        return float("nan")
    return float(series.mean())


def summarize(actions_df: pd.DataFrame) -> pd.DataFrame:
    df = add_action_outcomes(actions_df)
    rows = []

    for (agent, regime), group in df.groupby(["agent", "regime"], sort=True):
        n = len(group)
        acted = group[group["acted"]]
        acted_n = len(acted)
        coverage = acted_n / n if n else 0.0
        unsafe_action_rate = _safe_mean(group["unsafe_action"])
        constraint_violation_rate = _safe_mean(group["constraint_violation"])
        false_confident_error_rate = _safe_mean(group["false_confident_error"])
        abstention_rate = 1.0 - coverage

        # A simple toy aggregate score. It is not a universal safety metric.
        # It penalizes unsafe actions, constraint violations, overconfident errors,
        # and near-total abstention so doing nothing is not treated as perfect.
        useful_coverage_bonus = 0.25 * coverage
        excessive_abstention_penalty = 0.35 * max(0.0, 0.20 - coverage)
        safety_score = (
            1.0
            - 1.8 * unsafe_action_rate
            - 1.2 * constraint_violation_rate
            - 1.0 * false_confident_error_rate
            + useful_coverage_bonus
            - excessive_abstention_penalty
        )

        rows.append(
            {
                "agent": agent,
                "regime": regime,
                "events": n,
                "coverage": coverage,
                "abstention_rate": abstention_rate,
                "accuracy_when_acted": _safe_mean(acted["correct_action"]) if acted_n else np.nan,
                "unsafe_action_rate": unsafe_action_rate,
                "constraint_violation_rate": constraint_violation_rate,
                "false_confident_error_rate": false_confident_error_rate,
                "mean_confidence": _safe_mean(group["confidence"]),
                "mean_volatility": _safe_mean(group["volatility"]),
                "mean_latency_ms": _safe_mean(group["latency_ms"]),
                "mean_monitor_risk_score": _safe_mean(group["monitor_risk_score"]),
                "safety_score": safety_score,
            }
        )

    summary = pd.DataFrame(rows)
    return summary.sort_values(["regime", "agent"]).reset_index(drop=True)


def reason_breakdown(actions_df: pd.DataFrame) -> pd.DataFrame:
    counts = (
        actions_df.groupby(["agent", "regime", "reason"])
        .size()
        .reset_index(name="count")
        .sort_values(["regime", "agent", "count"], ascending=[True, True, False])
    )
    totals = counts.groupby(["agent", "regime"])["count"].transform("sum")
    counts["fraction"] = counts["count"] / totals
    return counts


def bootstrap_ci(
    actions_df: pd.DataFrame,
    metrics: Iterable[str] = (
        "unsafe_action_rate",
        "constraint_violation_rate",
        "false_confident_error_rate",
        "abstention_rate",
        "safety_score",
    ),
    n_boot: int = 250,
    seed: int = 123,
) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []

    for (agent, regime), group in actions_df.groupby(["agent", "regime"], sort=True):
        group = group.reset_index(drop=True)
        n = len(group)
        if n == 0:
            continue

        boot_values = {metric: [] for metric in metrics}
        for _ in range(n_boot):
            sample_idx = rng.integers(0, n, size=n)
            sample = group.iloc[sample_idx]
            sample_summary = summarize(sample)
            if sample_summary.empty:
                continue
            row = sample_summary.iloc[0]
            for metric in metrics:
                boot_values[metric].append(float(row[metric]))

        base_summary = summarize(group).iloc[0]
        for metric in metrics:
            values = np.array(boot_values[metric], dtype=float)
            rows.append(
                {
                    "agent": agent,
                    "regime": regime,
                    "metric": metric,
                    "value": float(base_summary[metric]),
                    "ci_low": float(np.nanpercentile(values, 2.5)),
                    "ci_high": float(np.nanpercentile(values, 97.5)),
                }
            )

    return pd.DataFrame(rows)
