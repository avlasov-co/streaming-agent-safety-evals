# Changelog

## 0.4.0

- Added explicit `ASK_OVERSIGHT` action support for episode evaluation.
- Added `OversightSeekingAgent` for escalation under multiple risk signals.
- Added `DriftDetector` and `ShiftAwareRiskAgent` for moving-window shift-aware risk gating.
- Expanded episode evaluation with trace-based accounting for oversight requests, useful/unnecessary oversight, repeated unsafe actions, total penalty, final risk, avoidable failures, and recovery after unsafe conditions.
- Kept the historical `run_episode()` compact return shape while adding `run_episode_trace()` for richer analysis.
- Added tests covering oversight actions, shift-aware escalation, backward-compatible episode returns, and the new episode summary columns.
- Added documentation for oversight-aware episode evaluation.

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

- Added generated figures, benchmark outputs, and core documentation.

## 0.1.0

- Initial public benchmark.
