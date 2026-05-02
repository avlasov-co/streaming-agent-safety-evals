# Reviewer Quickstart

## What this is

A small, runnable benchmark for evaluating agentic decision policies under distribution shift.

## What to inspect first

1. `README.md` for the top-level idea and result figures.
2. `docs/paper.md` for the paper-style writeup.
3. `docs/experimental_report.md` for the generated report.
4. `docs/eval_card.md`, `docs/threat_model.md`, and `docs/safety_case.md` for scope and safety framing.
5. `src/simulate.py`, `src/agents.py`, and `src/metrics.py` for the core event-stream implementation.
6. `fixtures/stream_cases.json`, `src/stream_monitor.py`, and `src/run_stream_demo.py` for the incremental partial-output/tool-call-like demo.
7. `src/run_multi_seed.py`, `src/sweep.py`, `src/run_episodes.py`, `src/static_vs_dynamic.py`, and `src/failure_replay.py` for deeper analysis utilities.

## Fast local run

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.run_eval --n-per-regime 300 --seed 42 --bootstrap 40
python -m src.plot_results
python -m src.generate_report
python -m src.run_stream_demo
python -m pytest -q
```

## Full smoke run

This exercises the core benchmark plus the newer analysis scripts:

```bash
python -m src.run_multi_seed --seeds 1 2 --n-per-regime 100
python -m src.sweep --n-per-regime 100
python -m src.run_episodes --n-episodes 5 --n-steps 20
python -m src.static_vs_dynamic --n-per-regime 100
python -m src.failure_replay --agent NaiveAgent --regime adversarial_shift --n-events 100 --n 5
python -m src.failure_replay --agent ConservativeAbstentionAgent --regime liquidity_crash --n-events 10 --n 5
python -m src.run_stream_demo
```

Or use Make:

```bash
make setup
make smoke
make test
```

## Main interpretation

The benchmark is intentionally simple. Its value is the evaluation pattern: dynamic regimes, unsafe behavior metrics, abstention/coverage tradeoffs, calibration analysis, failure replay, and explicit reporting of failure modes.


## Incremental stream demo interpretation

The stream demo is the only part of the repo that processes partial-output and tool-call-like records incrementally. It is intentionally deterministic and small. The current fixture set has four unsafe cases, two benign cases, one known false positive, zero premature interventions, and zero false negatives under the simple keyword/tool-pattern monitor.

Read the result as a stream-semantics smoke test: it checks whether unsafe evidence can be detected before the whole answer is complete, whether split chunks delay detection, whether tool-call-like events can be blocked before execution, whether benign safety discussion can still trigger a false positive, and whether early stops before fixture-labelled unsafe evidence are kept out of valid detections. It does **not** certify any deployed agent or classifier.
