# Roadmap for a 4‑Month Fellowship

This roadmap describes how the current benchmark could grow during a four‑month research fellowship.  The repository already contains the core streaming benchmark, a lightweight risk‑budget episode runner, threshold sweeps, multi‑seed evaluation, static-vs-dynamic comparison, failure replay, calibration plots, and documentation.  The goal of the roadmap is therefore not to invent those pieces from scratch, but to turn them into a richer agent safety evaluation framework.

## Weeks 1–2: Stabilize the research artifact

1. **Benchmark hardening**: Review the existing simulator, agents, metrics, plots, CI, and reproduction scripts.  Tighten documentation, improve naming, and make the artifact easy for an external reviewer to run.
2. **LLM-agent interface**: Add a small optional interface for language-model and tool-using agents.  Keep external API calls optional so the benchmark remains reproducible without credentials.
3. **Paper refinement**: Expand `docs/paper.md` from a mini-paper into a clearer research-style report with methodology, results, limitations, and future experiments.

## Weeks 3–4: Extend the existing episode system

1. **Richer multi-step episodes**: Expand the current risk-budget episode system beyond `failure_rate` and `mean_steps`.  Add metrics such as mean steps before failure, repeated unsafe action rate, total penalty, unsafe steps before failure, and recovery after shift.
2. **`ASK_OVERSIGHT` action**: Add an explicit oversight action and implement an `OversightSeekingAgent`.  Measure oversight request rate, avoidable failure rate, and unnecessary oversight rate.
3. **Basic drift detection**: Add a simple regime-shift detector using moving averages of volatility, latency, liquidity, and monitor risk.  Implement a `ShiftAwareRiskAgent` that tightens thresholds or asks oversight after detected shift.

## Month 2: Deepen dynamic evaluation analysis

1. **Pareto-frontier threshold analysis**: Expand the existing threshold sweep into a fuller Pareto-frontier analysis.  Sweep confidence thresholds, volatility limits, latency limits, liquidity floors, spread limits, and monitor risk limits.  Report coverage versus unsafe action rate and false-confident error rate.
2. **Calibration analysis**: Extend the current calibration bins and `figures/calibration_by_regime.png` with Brier scores, per-agent calibration plots, and acted-only calibration curves.
3. **Static-vs-dynamic extensions**: Extend the existing static-vs-dynamic comparison with richer scenario families, including mixed-regime trajectories and delayed shift detection.

## Month 3: Oversight and mitigation experiments

1. **Monitor failures**: Simulate monitor noise and blind spots.  Evaluate how monitor corruption affects unsafe actions.  Plot monitor ROC curves and compute monitor false negative rates.
2. **Counterfactual mitigation**: For each unsafe action by `NaiveAgent`, check whether risk gating, monitor gating, or oversight would have blocked it.  Compute blocked failure rate, missed failure rate, and avoidable failure rate.
3. **Adversarial scenario generators**: Add stress tests such as confidence inflation, latency spoofing, liquidity mirages, direction flips, and volatility masking.  Compare risk-gated and monitor policies under targeted attacks.

## Month 4: Release-quality research package

1. **Documentation polish**: Consolidate the documentation index, safety case, eval card, threat model, limitations, and result-reading guides into a clear reviewer path.
2. **Robustness runs**: Scale the existing multi-seed evaluation to more seeds and larger event counts.  Add robustness plots that show uncertainty across seeds.
3. **Benchmark release**: Tag a versioned release, write a changelog, freeze the reproducibility script, and prepare a short presentation or poster summarizing the benchmark and findings.

This roadmap keeps the project scoped.  It builds on the current working artifact and focuses on dynamic safety evaluation, oversight, calibration, and distribution-shift robustness rather than model training or production deployment.
