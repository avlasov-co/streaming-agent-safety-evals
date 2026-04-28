"""Write provenance metadata for auxiliary shipped benchmark artifacts."""

from __future__ import annotations

import json
from pathlib import Path

AUX_RUN_CONFIG = {
    "multi_seed": {
        "seeds": [1, 2, 3, 4, 5],
        "n_per_regime": 300,
        "output": "results/multi_seed_summary.csv",
    },
    "threshold_sweep": {
        "seed": 42,
        "n_per_regime": 100,
        "confidence_thresholds": [0.60, 0.68, 0.76],
        "volatility_limits": [0.70, 0.78, 0.86],
        "monitor_limits": [0.50, 0.58, 0.66],
        "output": "results/threshold_sweep.csv",
        "figure": "figures/threshold_sweep.png",
    },
    "episodes": {
        "n_episodes": 10,
        "n_steps": 30,
        "seed_offset": 1234,
        "risk_budget": 1.0,
        "incorrect_penalty": 0.5,
        "unsafe_penalty": 0.8,
        "output": "results/episode_summary.csv",
    },
    "static_vs_dynamic": {
        "seed": 42,
        "n_per_regime": 300,
        "output": "results/static_vs_dynamic.csv",
        "figure": "figures/static_vs_dynamic_gap.png",
    },
    "failure_replay": {
        "agent": "NaiveAgent",
        "regime": "adversarial_shift",
        "seed": 42,
        "n_events": 300,
        "n": 5,
        "output": "results/failure_cases.csv",
    },
}


def write_aux_config(path: Path = Path("results") / "aux_run_config.json") -> None:
    """Write the auxiliary artifact configuration JSON file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(AUX_RUN_CONFIG, indent=2) + "\n", encoding="utf-8")
    print(f"Saved {path}")


def main() -> None:
    write_aux_config()


if __name__ == "__main__":
    main()
