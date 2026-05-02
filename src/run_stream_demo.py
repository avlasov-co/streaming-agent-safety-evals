from __future__ import annotations

import argparse
from pathlib import Path

from .stream_monitor import evaluate_stream_cases, load_stream_cases, summarize_stream_results


RESULTS_DIR = Path("results")


def run(fixture: str | Path = "fixtures/stream_cases.json", output_dir: str | Path = RESULTS_DIR) -> None:
    """Run the deterministic incremental stream-monitoring demo."""
    out_dir = Path(output_dir)
    out_dir.mkdir(exist_ok=True)

    cases = load_stream_cases(fixture)
    case_results, event_results = evaluate_stream_cases(cases)
    summary = summarize_stream_results(case_results)

    case_path = out_dir / "stream_demo_cases.csv"
    event_path = out_dir / "stream_demo_events.csv"
    summary_path = out_dir / "stream_demo_summary.csv"
    case_results.to_csv(case_path, index=False)
    event_results.to_csv(event_path, index=False)
    summary.to_csv(summary_path, index=False)

    print(f"Saved {summary_path}")
    print(f"Saved {case_path}")
    print(f"Saved {event_path}")
    print()
    print("Aggregate stream-monitor metrics:")
    print(summary.to_string(index=False))
    print()
    print("Per-case results:")
    visible_columns = [
        "case_id",
        "expected_unsafe",
        "flagged",
        "false_positive",
        "false_negative",
        "premature_intervention",
        "detection_event",
        "time_to_detect_events",
        "unsafe_prefix_exposure_chars",
        "intervention_reason",
        "matched_pattern",
    ]
    print(case_results[visible_columns].to_string(index=False))


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the incremental stream-monitoring safety demo.")
    parser.add_argument("--fixture", default="fixtures/stream_cases.json", help="Path to stream-case fixture JSON")
    parser.add_argument("--output-dir", default=str(RESULTS_DIR), help="Directory for generated CSV outputs")
    args = parser.parse_args()
    run(fixture=args.fixture, output_dir=args.output_dir)


if __name__ == "__main__":
    main()
