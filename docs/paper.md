# Streaming Safety Evaluations for Agentic Decision Systems Under Distribution Shift

## Abstract

Modern AI systems increasingly act in dynamic environments where the data distribution can change rapidly and unpredictably.  Standard offline evaluations, which measure accuracy on a fixed test set, often fail to reveal the behavioural failures that surface when an agent must make decisions over time.  This mini‑paper introduces a lightweight benchmark for studying safety in agentic decision systems under distribution shift.  We synthesise streaming market‑like data across five regimes (normal, volatile, adversarial, latency spike and liquidity crash), implement several simple policies and measure unsafe actions, false‑confident errors, constraint violations, abstention and useful coverage.  We show that static accuracy is an insufficient indicator of safe deployment and that explicit risk gating, monitoring and abstention can reduce unsafe behaviour at the cost of coverage.  The benchmark is designed to be extensible to more complex agents and oversight mechanisms.

## Introduction

Large language models and other AI systems are increasingly being integrated into agentic workflows, from code assistants to autonomous trading strategies.  These agents interact with a non‑stationary environment, ingest streaming observations and must decide whether to act, abstain or defer to oversight.  Safety failures—wrong actions taken with high confidence under unfamiliar conditions—pose significant risks when such systems are deployed in high‑stakes settings.  Most existing evaluations measure model accuracy on a static test set, which can hide over‑confidence, brittleness and risk‑taking behaviour.  To make progress on agent safety, we need benchmarks that simulate deployment conditions, measure unsafe actions directly and allow experimentation with mitigations such as abstention, monitoring and oversight.

## Benchmark Design

The benchmark generates synthetic streaming data resembling a limit‑order‑book environment.  For each of five regimes—normal, volatile, adversarial shift, latency spike and liquidity crash—1000–3000 events are synthesised.  Each event contains the true direction (1 or −1), a model’s predicted direction, a confidence score, market volatility, network latency, liquidity, bid–ask spread, order imbalance, a drift term and a synthetic monitor risk score.  The regimes differ in correctness probability and how confidence relates to correctness and risk.  In the adversarial regime, for example, confidence remains high even when the prediction is often wrong.

We implement several lightweight policies:

* **NaiveAgent**: always acts on the model prediction.
* **ConfidenceThresholdAgent**: abstains when confidence is below a threshold.
* **RiskGatedAgent**: abstains when confidence, volatility, latency, liquidity or spread indicate elevated risk.
* **MonitorThenActAgent**: uses a separate monitor risk score to block actions even when confidence is high.
* **ConservativeAbstentionAgent**: combines several conservative checks and rarely acts.

These policies are intentionally simple; the goal is to expose safety failure modes and compare the effects of gating and monitoring.

## Metrics

Each run produces an `actions` table where every row contains the event features, the agent name, the chosen action and a reason code.  From this table we compute:

* **coverage**: fraction of events where the agent acted (not abstained).
* **accuracy_when_acted**: accuracy on the events where the agent acted.
* **unsafe_action_rate**: proportion of all events where the agent acted incorrectly.
* **constraint_violation_rate**: proportion of actions taken during explicitly unsafe conditions (high volatility, high latency, low liquidity or wide spread).
* **false_confident_error_rate**: high‑confidence wrong actions (confidence ≥ 0.70 and incorrect action).
* **abstention_rate**: fraction of events where the agent abstained.
* **ece_all** and **ece_when_acted**: simple bin‑based expected calibration errors across all events and acted events, respectively.
* **toy_safety_score**: an illustrative aggregate score that penalises unsafe behaviour, over‑confidence and near‑total abstention and rewards useful coverage.

Bootstrap confidence intervals for key metrics are computed by resampling the `actions` table.

## Results

Across regimes, the **NaiveAgent** achieves high coverage but exhibits the highest unsafe action rate and false‑confident error rate.  The **ConfidenceThresholdAgent** reduces unsafe actions by abstaining when confidence is low, but still suffers from elevated failure rates in adversarial and volatile regimes.  The **RiskGatedAgent** and **MonitorThenActAgent** substantially reduce unsafe actions and constraint violations by abstaining during high‑risk conditions.  However, these mitigations reduce coverage, particularly in the conservative abstention strategy.  A small but non‑zero abstention threshold is necessary: the **ConservativeAbstentionAgent** attains near‑perfect safety by abstaining on almost all events, which is useless in practice.

Our results show that static accuracy (evaluated on the normal regime) correlates poorly with safety metrics under distribution shift.  Agents that achieve similar accuracy in the normal regime can diverge significantly in unsafe action rate in adversarial and latency‑spike regimes.  This underscores the need for dynamic evaluations that reflect deployment conditions.

## Limitations

This benchmark uses synthetic data and simple rule‑based policies.  The regimes are stylised and may not capture all dynamics of real markets or other deployment environments.  The toy safety score is a heuristic illustration, not a universal metric.  The current version includes lightweight multi‑step risk-budget episodes and threshold sweeps, but these are still first-pass analyses rather than full sequential decision environments.  The agents do not learn from feedback and there is not yet a mechanism for asking oversight or escalating to a human.  Our evaluation is therefore a first step towards more comprehensive agent safety benchmarks.

## Future Work

The current version already includes a lightweight first pass at multi‑step risk-budget episodes, threshold sweeps, static-vs-dynamic comparison, multi-seed robustness, calibration plots, and failure replay.  Future work should make these richer: add explicit **ASK_OVERSIGHT** actions, implement drift detection and adaptive risk thresholds, evaluate LLM-based or tool-using agents, introduce adversarial scenario generators, assess monitor failures, and expand the sweep analysis into clearer Pareto-frontier evaluation.  A critical extension is adding a regime shift detector so that agents can respond to changing conditions rather than relying on static thresholds.

## Conclusion

Static evaluations can overestimate the safety of agentic decision systems by ignoring how the environment changes over time.  Our benchmark provides a simple yet extensible platform for studying safety metrics under distribution shift.  By simulating different regimes and comparing policies that abstain, gate or monitor, we reveal failures that static accuracy obscures and explore the tradeoffs between safety and coverage.  We hope this work encourages researchers and engineers to design evaluations that reflect real deployment conditions and to develop mitigations such as oversight and dynamic risk management.