# Streaming Safety Evaluations for Agentic AI Systems Under Distribution Shift

## Research question

How can we evaluate agentic AI systems that behave safely not only on static test sets, but also in sequential environments where the data distribution changes over time?

## Motivation

Many AI evaluations are static. They measure model performance on a fixed dataset. This can miss failures that appear only when an agent acts repeatedly in a changing environment.

Deployed AI systems may face latency, noise, adversarial inputs, distribution shift, uncertain feedback, and pressure to act quickly. In those settings, a model can appear competent in normal conditions but become unsafe when confidence remains high while correctness drops.

## Existing prototype

This repository implements a minimal no-training benchmark. It uses synthetic streaming events and simple policy agents to study safety-relevant failure modes.

The benchmark compares:

- a naive agent that always acts
- a confidence-threshold agent that abstains under low confidence
- a risk-gated agent that abstains under high volatility, high latency, low liquidity, wide spread, or low confidence
- a monitor-then-act agent that uses a separate risk score
- a conservative abstention agent that acts only under favorable conditions

## Fellowship-scale extension

The current repository already includes a runnable core benchmark, lightweight risk-budget episodes, threshold sweeps, multi-seed evaluation, static-vs-dynamic comparison, calibration artifacts, and failure replay.  A fellowship-scale version would expand those first-pass components into a deeper agent safety evaluation framework:

1. Replace or supplement rule-based agents with LLM/tool-using agents.
2. Expand the existing episode system into richer sequential tasks where agents must plan, revise actions, recover after shift, and decide when to defer.
3. Add an explicit `ASK_OVERSIGHT` action and evaluate oversight request rate, avoidable failure rate, and unnecessary oversight.
4. Extend the existing static-vs-dynamic comparison with mixed-regime trajectories, drift detection, and stronger adversarial scenario families.
5. Evaluate monitor agents, uncertainty gates, policy constraints, and counterfactual mitigation.
6. Release an open benchmark, metrics suite, and research writeup.
