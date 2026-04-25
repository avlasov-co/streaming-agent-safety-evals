# Streaming Agent Safety Evaluations

A no-training benchmark for evaluating agentic decision systems under distribution shift, uncertainty, latency spikes, and adversarial perturbations.

This project tests a simple safety question: **what happens when an agent keeps acting confidently after the environment changes?**

The benchmark uses synthetic streaming data and lightweight rule-based agents. It measures unsafe actions, false-confident errors, constraint violations, abstention, and the tradeoff between acting often and acting safely.

This repository does **not** contain proprietary Polinash code, private datasets, model weights, trading logic, exchange integrations, API keys, or financial advice. It is a public research artifact focused on safety evaluation design.

## Project highlights

- No-training benchmark focused on safety evaluation, not model scale
- Simulates deployment regimes where confidence can stay high while correctness drops
- Compares always-act, confidence-threshold, risk-gated, monitor-based, and conservative abstention policies
- Measures unsafe action rate, false-confident error rate, constraint violations, abstention, and coverage
- Includes generated results, plots, tests, and an experimental report

## Why this exists

Many AI evaluations are static. They test performance on fixed datasets. Deployed agentic systems are different: they act repeatedly, receive changing inputs, operate under uncertainty, and may face adversarial or shifted conditions.

This benchmark demonstrates how dynamic evaluations can reveal failures that static accuracy metrics may miss: overconfident errors, unsafe actions under distribution shift, and constraint violations during risky conditions.

## Example results

### Unsafe action rate

![Unsafe action rate](figures/unsafe_action_rate.png)

### False confident error rate

![False confident error rate](figures/false_confident_error_rate.png)

### Safety tradeoff

![Abstention tradeoff](figures/abstention_tradeoff.png)

## Report and reproduction

- [Experimental report](docs/experimental_report.md)
- [Safety relevance notes](docs/safety_relevance.md)
- [Fellowship application summary](docs/fellowship_application_summary.md)

Reproduce the benchmark:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.run_eval --n-per-regime 3000 --seed 42 --bootstrap 250
python -m src.plot_results
python -m src.generate_report
python -m pytest -q
