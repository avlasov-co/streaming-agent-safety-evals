# Fellowship Application Summary

## One-line summary

I built a no-training benchmark for evaluating whether agentic decision systems become unsafe under distribution shift, especially when confidence remains high while correctness drops.

## Why I built this

My private ML systems work exposed me to practical problems in non-stationary streaming environments: distribution shift, latency, noisy inputs, confidence failures, evaluation leakage, and robustness under changing conditions.

This repository abstracts those problems into a public safety-evaluation benchmark without exposing proprietary code, private datasets, model weights, or production logic.

## What the benchmark shows

The benchmark compares several simple agent policies across normal, volatile, adversarial-shift, latency-spike, and liquidity-crash regimes.

It shows that always-act policies can maintain high coverage but produce unsafe actions under shift. Risk-aware and monitor-based policies can reduce unsafe actions and false-confident errors, but at the cost of lower coverage. Conservative abstention shows why reporting coverage matters: never acting can look safe, but is not a complete deployment solution.

## Current implemented extensions

- Core streaming benchmark across five regimes
- Calibration metrics and calibration plot
- Static-vs-dynamic comparison
- Threshold sweep analysis
- Multi-seed robustness analysis
- Lightweight multi-step risk-budget episodes
- Failure replay for inspecting concrete unsafe actions
- Paper-style report, evaluation card, threat model, and safety case

## What I would extend during the fellowship

- Add LLM/tool-using agents
- Add explicit oversight actions such as `ASK_OVERSIGHT`
- Add drift detection and shift-aware agents
- Add stronger monitor and oversight methods
- Expand the episode system with richer recovery and repeated-failure metrics
- Study abstention, deferral, and autonomy tradeoffs
- Release an open benchmark and research writeup
