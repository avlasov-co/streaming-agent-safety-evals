# Safety Case

This document gives the argument behind the benchmark: dynamic safety evaluations are necessary because static evaluations can hide unsafe agent behaviour under distribution shift.

## Claim

Static accuracy is not enough to evaluate agentic systems. A system can look capable on a fixed test set while acting unsafely when the environment changes.

## Evidence from this benchmark

### Confidence can remain high while correctness drops

The adversarial-shift regime is designed so confidence remains elevated even when predictions become less reliable. This creates false-confident errors, where an agent takes an incorrect action with high confidence.

### Risk gating reduces unsafe actions

The `RiskGatedAgent` blocks actions when confidence, volatility, latency, liquidity, or spread indicate elevated risk. This reduces unsafe actions and constraint violations, but it also reduces coverage. That is the central safety-performance tradeoff.

### Total abstention is not a real solution

The `ConservativeAbstentionAgent` often achieves very low unsafe action rates by acting rarely. This is safer but less useful. A serious evaluation must report both safety and coverage.

### Static and dynamic evaluations diverge

`src/static_vs_dynamic.py` compares normal-regime behaviour to all-regime behaviour. The gap shows why normal-regime accuracy cannot be treated as deployment safety.

## Assumptions

- The data is synthetic.
- The agents are simple rule-based policies.
- The monitor score is an imperfect synthetic proxy.
- The toy safety score is diagnostic, not normative.

## Limitations

This benchmark does not certify real systems. It does not use live trading data, real exchange integrations, proprietary model weights, or production logic. It is a research artifact for studying failure modes and mitigation patterns.

## Future evidence needed

The safety case would be stronger with LLM-based agents, explicit `ASK_OVERSIGHT` actions, human-in-the-loop simulations, drift-aware adaptive policies, stronger adversarial scenario generators, and richer multi-step tasks.
