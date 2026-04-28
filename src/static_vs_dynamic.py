"""
Compare static versus dynamic evaluation of streaming decision agents.

Static evaluation uses only the normal regime and asks: "how accurate is the
agent when conditions look normal?" Dynamic evaluation uses all regimes and
asks: "how unsafe does the agent become when the environment changes?"

This script writes:

- results/static_vs_dynamic.csv
- figures/static_vs_dynamic_gap.png
"""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Dict, List

import matplotlib.pyplot as plt
import pandas as pd

from .agents import default_agents
from .metrics import add_action_outcomes
from .simulate import generate_dataset


RESULTS_DIR = Path("results")
FIGURES_DIR = Path("figures")


def _evaluate_agent(agent, events: pd.DataFrame) -> pd.DataFrame:
    rows = []
    for _, row in events.iterrows():
        decision = agent.decide(row)
        rows.append({**row.to_dict(), "agent": agent.name, "action": decision["action"], "reason": decision["reason"]})
    return add_action_outcomes(pd.DataFrame(rows))


def _metrics_from_actions(actions: pd.DataFrame) -> Dict[str, float]:
    acted = actions[actions["acted"]]
    return {
        "accuracy_when_acted": float(acted["correct_action"].mean()) if len(acted) else float("nan"),
        "unsafe_action_rate": float(actions["unsafe_action"].mean()) if len(actions) else float("nan"),
        "constraint_violation_rate": float(actions["constraint_violation"].mean()) if len(actions) else float("nan"),
        "coverage": float(actions["acted"].mean()) if len(actions) else float("nan"),
    }


def compare_static_dynamic(n_per_regime: int = 3000, seed: int = 42) -> pd.DataFrame:
    """Run static and dynamic evaluations for every default agent.

    Static evaluation includes only the ``normal`` regime. Dynamic evaluation
    includes all regimes. Metrics are computed over the actual acted samples,
    not by unweighted averaging over regimes.
    """
    events = generate_dataset(n_per_regime=n_per_regime, seed=seed)
    static_events = events[events["regime"] == "normal"].copy()
    dynamic_events = events.copy()

    rows: List[Dict[str, float]] = []
    for agent in default_agents():
        static_actions = _evaluate_agent(agent, static_events)
        dynamic_actions = _evaluate_agent(agent, dynamic_events)
        static_m = _metrics_from_actions(static_actions)
        dynamic_m = _metrics_from_actions(dynamic_actions)
        rows.append(
            {
                "agent": agent.name,
                "static_accuracy_when_acted": static_m["accuracy_when_acted"],
                "dynamic_accuracy_when_acted": dynamic_m["accuracy_when_acted"],
                "static_unsafe_action_rate": static_m["unsafe_action_rate"],
                "dynamic_unsafe_action_rate": dynamic_m["unsafe_action_rate"],
                "static_constraint_violation_rate": static_m["constraint_violation_rate"],
                "dynamic_constraint_violation_rate": dynamic_m["constraint_violation_rate"],
                "static_coverage": static_m["coverage"],
                "dynamic_coverage": dynamic_m["coverage"],
                "accuracy_gap": static_m["accuracy_when_acted"] - dynamic_m["accuracy_when_acted"],
                "unsafe_rate_increase": dynamic_m["unsafe_action_rate"] - static_m["unsafe_action_rate"],
            }
        )
    return pd.DataFrame(rows)


def plot_gap(df: pd.DataFrame, out_path: Path) -> None:
    """Plot dynamic unsafe-action increase and accuracy drop per agent."""
    ax = df.set_index("agent")[["accuracy_gap", "unsafe_rate_increase"]].plot(kind="bar", figsize=(10, 5))
    ax.set_title("Static vs dynamic evaluation gap")
    ax.set_xlabel("Agent")
    ax.set_ylabel("Gap")
    plt.xticks(rotation=25, ha="right")
    plt.tight_layout()
    out_path.parent.mkdir(exist_ok=True)
    plt.savefig(out_path, dpi=170)
    plt.close()


def main() -> None:
    parser = argparse.ArgumentParser(description="Compare static and dynamic evaluations for streaming agents.")
    parser.add_argument("--n-per-regime", type=int, default=3000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--no-plot", action="store_true", help="Do not generate the gap figure.")
    parser.add_argument(
        "--output",
        type=str,
        default=str(RESULTS_DIR / "static_vs_dynamic.csv"),
        help="Where to write the static vs dynamic comparison CSV",
    )
    args = parser.parse_args()
    RESULTS_DIR.mkdir(exist_ok=True)
    df = compare_static_dynamic(n_per_regime=args.n_per_regime, seed=args.seed)
    out_path = Path(args.output)
    df.to_csv(out_path, index=False)
    print(f"Saved static vs dynamic comparison to {out_path}")
    if not args.no_plot:
        FIGURES_DIR.mkdir(exist_ok=True)
        plot_path = FIGURES_DIR / "static_vs_dynamic_gap.png"
        plot_gap(df, plot_path)
        print(f"Saved {plot_path}")
    print()
    print(df.to_string(index=False))


if __name__ == "__main__":
    main()
