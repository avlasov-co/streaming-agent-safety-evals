# Failure Taxonomy

This benchmark focuses on safety-relevant behavioral failures in sequential decision systems.

## 1. Overconfident error

The agent takes a wrong action while confidence is high.

Metric: `false_confident_error_rate`

Why it matters: high confidence can cause downstream systems or users to trust a bad action.

## 2. Constraint violation

The agent acts during conditions marked unsafe by external constraints.

Metric: `constraint_violation_rate`

Why it matters: some conditions should trigger deferral even if the model predicts a favorable action.

## 3. Unsafe action under shift

The agent takes a wrong action in a shifted regime.

Metric: `unsafe_action_rate` by regime

Why it matters: static tests can hide deployment failures.

## 4. Excessive abstention

The agent refuses too often, reducing usefulness.

Metric: `abstention_rate`

Why it matters: safety mechanisms must be useful enough to deploy.

## 5. Monitor failure

A monitoring or gating mechanism fails to block risky actions.

Metric: remaining unsafe actions after monitor gating

Why it matters: oversight systems need their own evaluation, not blind trust.
