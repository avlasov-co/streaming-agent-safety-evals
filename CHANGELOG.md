# Changelog

## 0.3.0

- Added incremental stream-demo metric names: `intervention_rate` and `valid_detection_rate`.
- Added `premature_interventions` accounting so early stops before fixture-labelled unsafe evidence do not inflate valid detections.
- Added multi-seed evaluation.
- Added threshold sweep utility.
- Added multi-step episode simulation.
- Added static-vs-dynamic comparison.
- Added failure replay.
- Added calibration bins and calibration plot.
- Added safety case, evaluation card, threat model, paper, result-reading guide, and documentation index.
- Renamed the aggregate score to `toy_safety_score` to avoid overclaiming.

## 0.2.0

- Added generated figures, benchmark outputs, CI, and core documentation.

## 0.1.0

- Initial public benchmark.
