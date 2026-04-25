# Streaming Safety Evaluations for Agentic AI Systems Under Distribution Shift

## Research question

How can we evaluate agentic AI systems that behave safely not only on static test sets, but also in sequential environments where the data distribution changes over time?

## Motivation

Many AI evaluations are static. They measure model performance on a fixed dataset. This can miss failures that appear only when an agent acts repeatedly in a changing environment.

Deployed AI systems may face latency, noise, adversarial inputs, distribution shift, uncertain feedback, and pressure to act quickly. In those settings, a model can appear competent in normal conditions but become unsafe when confidence remains high while correctness drops.

## Prototype

This repository implements a minimal no-training benchmark. It uses synthetic streaming events and simple policy agents to study safety-relevant failure modes.

The benchmark compares:

- a naive agent that always acts
- a confidence-threshold agent that abstains under low confidence
- a risk-gated agent that abstains under high volatility, high latency, low liquidity, wide spread, or low confidence
- a monitor-then-act agent that uses a separate risk score
- a conservative abstention agent that acts only under favorable conditions

The environment contains multiple regimes:

- normal
- volatile
- adversarial shift
- latency spike
- liquidity crash

## Safety metrics

The benchmark measures:

- unsafe action rate
- false confident error rate
- constraint violation rate
- abstention rate
- coverage
- accuracy when acted
- aggregate toy safety score

## Expected fellowship extension

A fellowship-scale version would extend this prototype in several ways:

1. Replace simple policy agents with stronger LLM-based or tool-using agents.
2. Add richer sequential tasks where agents must plan over multiple steps.
3. Evaluate oversight methods such as uncertainty gating, policy constraints, monitor agents, and deferral policies.
4. Study whether static evaluations predict dynamic deployment failures.
5. Release an open benchmark, metrics suite, and research writeup.

## Expected output

- Open-source benchmark
- Baseline agents
- Safety metrics suite
- Experimental report
- Dataset/simulation generator
- Extension path for LLM-based agent evaluations
