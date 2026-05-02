# Methodology

## Environment

The benchmark generates synthetic streaming events across five regimes:

- normal
- volatile
- adversarial shift
- latency spike
- liquidity crash

Each event contains a true direction, a predicted direction, a confidence value, volatility, latency, liquidity, spread, drift, order imbalance, and a monitor risk score.

## Why synthetic data

Synthetic data keeps the benchmark public, reproducible, and free of proprietary datasets. The goal is not to model a real market perfectly. The goal is to produce controlled failure modes that resemble general deployment problems in sequential agent systems.

## Agents

The agents are lightweight policies:

- always act
- abstain under low confidence
- abstain under risk gates
- use a monitor score
- conservative multi-condition abstention

These agents are not meant to be strong. They are meant to make failure modes and mitigation tradeoffs easy to inspect.

## Metrics

The benchmark focuses on safety-relevant behavior:

- unsafe action rate
- false-confident error rate
- constraint violation rate
- abstention rate
- useful coverage
- accuracy when acted
- illustrative safety score

## Bootstrap intervals

The runner generates bootstrap confidence intervals for selected metrics. These intervals are not a substitute for deeper statistical analysis, but they make result variance visible instead of hiding it behind single numbers.


## Incremental stream-monitor demo

The repo also includes a small deterministic demo for real-time partial-output and tool-call-like monitoring. Cases live in `fixtures/stream_cases.json`. The runner `python -m src.run_stream_demo` feeds each event into `IncrementalSafetyMonitor` one at a time and stops when the monitor intervenes.

The demo covers:

- unsafe partial output that appears before a later refusal
- unsafe content appearing late in an otherwise benign stream
- unsafe phrases split across chunks, causing delayed detection
- tool-call-like records that should be blocked before execution
- a benign policy sentence that is intentionally false-positive flagged
- a benign stream that should pass

The monitor uses deterministic keyword/tool-pattern matching. That is intentionally limited. The useful artifact is the stream-processing interface, fixtures, confusion-matrix accounting, premature-intervention accounting, time-to-detect metric, and unsafe-prefix exposure metric.
