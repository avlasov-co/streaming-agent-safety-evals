# How to Read the Results

This benchmark reports several metrics because no single number can describe safe agent behaviour. A policy that never acts can look safe, but it is not useful. A policy that always acts can look useful, but it may be reckless under shift.

## Main output files

- `results/summary.csv`: one row per agent and regime.
- `results/summary_with_ci.csv`: bootstrap confidence intervals for key metrics.
- `results/reason_breakdown.csv`: why each agent acted or abstained.
- `results/calibration_bins.csv`: confidence bins and empirical correctness per regime.
- `results/static_vs_dynamic.csv`: normal-regime evaluation compared with all-regime evaluation.
- `results/threshold_sweep.csv`: risk-threshold tradeoff sweep.
- `results/multi_seed_summary.csv`: mean and standard deviation across seeds.
- `results/episode_summary.csv`: multi-step episode failure rates.
- `results/failure_cases.csv`: concrete high-risk failure examples.

## Metrics that matter most

### Coverage

`coverage` is the fraction of events where the agent acts. Higher coverage means the agent is more useful, but only if it remains safe. Near-zero coverage usually means the agent is avoiding risk by doing almost nothing.

### Unsafe action rate

`unsafe_action_rate` is the fraction of all events where the agent acted incorrectly. This is one of the main hazard metrics. A high value means the policy is taking bad actions, not merely making harmless prediction errors.

### Constraint violation rate

`constraint_violation_rate` counts actions taken during explicit unsafe conditions, such as high volatility, high latency, low liquidity, or wide spread. This measures whether the agent respects operational risk constraints.

### False-confident error rate

`false_confident_error_rate` counts wrong actions made with confidence at or above 0.70. This captures the dangerous case where the system is wrong and confident.

### Expected calibration error

`ece_all` and `ece_when_acted` compare confidence against empirical correctness. A high ECE means confidence is not aligned with reality. In adversarial or shifted regimes, this often reveals that the agent remains confident after the environment changes.

### Toy safety score

`toy_safety_score` is an illustrative aggregate score. It penalizes unsafe actions, constraint violations, overconfident errors, and near-total abstention. It is useful for quick comparison, but it is not a universal safety metric and should never replace the raw metrics.

## How to interpret agents

- `NaiveAgent` is the reckless baseline. It acts on every prediction.
- `ConfidenceThresholdAgent` tests whether confidence alone is enough.
- `RiskGatedAgent` tests explicit operational constraints.
- `MonitorThenActAgent` tests a separate monitor signal.
- `ConservativeAbstentionAgent` shows the limit case: very low risk through very low coverage.

## Common traps

Do not rank agents only by `toy_safety_score`. Inspect coverage and unsafe action rate together.

Do not assume high `accuracy_when_acted` means the agent is safe. A policy can abstain on hard cases and act only on easy cases.

Do not treat normal-regime performance as deployment safety. The core point of this benchmark is that shifted regimes expose failures hidden by static evaluation.
