# Limitations and Future Work

## Limitations

- The environment is synthetic.
- The agents are simple rule-based policies.
- The benchmark does not yet include LLM-based or tool-using agents.
- The incremental stream demo uses toy partial-output and tool-call-like fixtures, not live provider streams or real tool execution.
- The stream monitor is deterministic keyword/tool-pattern matching, not a robust classifier.
- The toy safety score is illustrative and should not replace direct inspection of the underlying metrics.
- The simulator abstracts away many real deployment complexities.
- The current episode system is intentionally lightweight: it tracks risk-budget failure rate and mean steps, but it does not yet model recovery, rich delayed feedback, or multi-agent oversight.

## Why the benchmark is still useful

The point is not realism by itself. The point is to demonstrate a public, reproducible evaluation pattern for agent behavior under distribution shift.

The project asks whether an agent keeps acting when it should abstain, whether confidence remains useful under shift, and whether basic oversight methods reduce unsafe behavior. It now includes a first pass at several deeper analysis tools: multi-step risk-budget episodes, threshold sweeps, static-vs-dynamic comparisons, calibration plots, multi-seed robustness, and failure replay.

## Implemented extensions

- Multi-step risk-budget episodes via `src.run_episodes`
- Static-vs-dynamic comparison via `src.static_vs_dynamic`
- Threshold sweep analysis via `src.sweep`
- Multi-seed robustness via `src.run_multi_seed`
- Calibration bins and calibration plot via `src.plot_results`
- Incremental stream-monitor demo via `src.run_stream_demo` and `fixtures/stream_cases.json`
- Paper-style report in `docs/paper.md`
- Safety case, threat model, and evaluation card in `docs/`

## Future work

- Replace or compare the simple stream monitor with semantic classifiers
- Add live-provider stream adapters while keeping deterministic fixtures for CI
- Add LLM/tool-using agents
- Add explicit `ASK_OVERSIGHT` actions and an `OversightSeekingAgent`
- Add drift detection and a `ShiftAwareRiskAgent`
- Add richer episode metrics such as repeated unsafe action rate, total penalty, and recovery after shift
- Add stronger monitor agents and monitor-failure experiments
- Add richer uncertainty and calibration metrics
- Add ablations over autonomy levels
- Add adversarial scenario generators rather than only adversarial-style distribution shifts
- Expand threshold sweeps into clearer Pareto frontier analysis
