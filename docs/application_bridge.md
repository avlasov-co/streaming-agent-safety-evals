# Application Bridge

This document explains how this repository should be framed in a fellowship application.

## One-line description

I built a no-training benchmark for evaluating whether agentic decision systems become unsafe under distribution shift, especially when confidence remains high while correctness drops.

## Why this is relevant

The project demonstrates evaluation design, not model scale. It shows how to create deployment regimes, define safety metrics, compare mitigations, and report tradeoffs between useful action and abstention.

## Connection to private engineering work

My private work on real-time ML systems exposed me to practical problems in non-stationary streaming environments: distribution shift, latency, noisy inputs, confidence failures, evaluation leakage, and robustness under changing conditions. This public benchmark abstracts those lessons into a safety-relevant evaluation setting without exposing proprietary code or data.

## What I would extend during a fellowship

- Add LLM/tool-using agents.
- Add multi-step sequential tasks.
- Add stronger monitor and oversight methods.
- Compare static test performance against dynamic deployment behavior.
- Release an open benchmark and writeup.
