This repository implements a small, runnable safety-evaluation benchmark for agentic decision systems. It simulates non-stationary streaming environments where confidence can remain high while correctness drops, then compares simple agent policies such as always-act, confidence-thresholding, risk-gating, monitoring, and conservative abstention.

The goal is not to train a large model or optimize trading performance. The goal is to demonstrate how dynamic evaluations can reveal failures that static accuracy metrics may miss: overconfident errors, unsafe actions under distribution shift, and constraint violations during risky conditions.


# Streaming Agent Safety Evaluations

A no-training benchmark for evaluating agentic decision systems under distribution shift, uncertainty, latency spikes, and adversarial perturbations.

This project tests a simple safety question: what happens when an agent keeps acting confidently after the environment changes?

The benchmark uses synthetic streaming data and lightweight rule-based agents. It measures unsafe actions, false-confident errors, constraint violations, abstention, and the tradeoff between acting often and acting safely.

This repository does not contain proprietary Polinash code, private datasets, model weights, trading logic, exchange integrations, API keys, or financial advice. It is a public research artifact focused on safety evaluation design.
