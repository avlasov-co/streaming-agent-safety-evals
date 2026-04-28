# Experimental Report

## Summary

This report summarizes a no-training benchmark for evaluating agentic decision behavior under distribution shift. The benchmark compares simple agents that either always act, abstain under low confidence, or use risk/monitoring gates before acting.

The main finding is expected and safety-relevant: agents that always act maintain high coverage but show worse unsafe-action behavior under shifted regimes. Agents with abstention or monitoring reduce unsafe actions, but pay for it with lower coverage.

## Full summary table

| agent                       | regime            |   events |   coverage |   abstention_rate |   accuracy_when_acted |   unsafe_action_rate |   constraint_violation_rate |   false_confident_error_rate |   ece_all |   ece_when_acted |   mean_confidence |   mean_volatility |   mean_latency_ms |   mean_monitor_risk_score |   toy_safety_score |
|:----------------------------|:------------------|---------:|-----------:|------------------:|----------------------:|---------------------:|----------------------------:|-----------------------------:|----------:|-----------------:|------------------:|------------------:|------------------:|--------------------------:|-------------------:|
| ConfidenceThresholdAgent    | adversarial_shift |     3000 |     0.8777 |            0.1223 |                0.5397 |               0.404  |                      0.747  |                       0.3733 |    0.26   |           0.2644 |            0.783  |            0.8605 |           32.4288 |                    0.617  |            -0.8833 |
| ConservativeAbstentionAgent | adversarial_shift |     3000 |     0.0023 |            0.9977 |                0.8571 |               0.0003 |                      0.0007 |                       0.0003 |    0.26   |           0.1384 |            0.783  |            0.8605 |           32.4288 |                    0.617  |             0.8743 |
| MonitorThenActAgent         | adversarial_shift |     3000 |     0.47   |            0.53   |                0.5291 |               0.2213 |                      0.3627 |                       0.192  |    0.26   |           0.2672 |            0.783  |            0.8605 |           32.4288 |                    0.617  |            -0.015  |
| NaiveAgent                  | adversarial_shift |     3000 |     1      |            0      |                0.523  |               0.477  |                      0.8537 |                       0.3733 |    0.26   |           0.26   |            0.783  |            0.8605 |           32.4288 |                    0.617  |            -1.1103 |
| RiskGatedAgent              | adversarial_shift |     3000 |     0.098  |            0.902  |                0.5952 |               0.0397 |                      0      |                       0.0357 |    0.26   |           0.2096 |            0.783  |            0.8605 |           32.4288 |                    0.617  |             0.7979 |
| ConfidenceThresholdAgent    | latency_spike     |     3000 |     0.4583 |            0.5417 |                0.6909 |               0.1417 |                      0.3717 |                       0.126  |    0.1003 |           0.0976 |            0.6666 |            0.6039 |           87.3221 |                    0.6207 |             0.2486 |
| ConservativeAbstentionAgent | latency_spike     |     3000 |     0.0037 |            0.9963 |                0.5455 |               0.0017 |                      0.0007 |                       0.0017 |    0.1003 |           0.3318 |            0.6666 |            0.6039 |           87.3221 |                    0.6207 |             0.794  |
| MonitorThenActAgent         | latency_spike     |     3000 |     0.2917 |            0.7083 |                0.6514 |               0.1017 |                      0.1977 |                       0.062  |    0.1003 |           0.1006 |            0.6666 |            0.6039 |           87.3221 |                    0.6207 |             0.5505 |
| NaiveAgent                  | latency_spike     |     3000 |     1      |            0      |                0.5663 |               0.4337 |                      0.817  |                       0.126  |    0.1003 |           0.1003 |            0.6666 |            0.6039 |           87.3221 |                    0.6207 |            -0.6771 |
| RiskGatedAgent              | latency_spike     |     3000 |     0.0837 |            0.9163 |                0.7092 |               0.0243 |                      0      |                       0.023  |    0.1003 |           0.1062 |            0.6666 |            0.6039 |           87.3221 |                    0.6207 |             0.8709 |
| ConfidenceThresholdAgent    | liquidity_crash   |     3000 |     0.56   |            0.44   |                0.6792 |               0.1797 |                      0.5343 |                       0.1577 |    0.123  |           0.1068 |            0.6986 |            0.697  |           47.2744 |                    0.6823 |            -0.025  |
| ConservativeAbstentionAgent | liquidity_crash   |     3000 |     0      |            1      |              nan      |               0      |                      0      |                       0      |    0.123  |         nan      |            0.6986 |            0.697  |           47.2744 |                    0.6823 |             0.93   |
| MonitorThenActAgent         | liquidity_crash   |     3000 |     0.201  |            0.799  |                0.6783 |               0.0647 |                      0.179  |                       0.042  |    0.123  |           0.0838 |            0.6986 |            0.697  |           47.2744 |                    0.6823 |             0.6435 |
| NaiveAgent                  | liquidity_crash   |     3000 |     1      |            0      |                0.5757 |               0.4243 |                      0.9553 |                       0.1577 |    0.123  |           0.123  |            0.6986 |            0.697  |           47.2744 |                    0.6823 |            -0.8671 |
| RiskGatedAgent              | liquidity_crash   |     3000 |     0.0243 |            0.9757 |                0.7671 |               0.0057 |                      0      |                       0.0047 |    0.123  |           0.0617 |            0.6986 |            0.697  |           47.2744 |                    0.6823 |             0.905  |
| ConfidenceThresholdAgent    | normal            |     3000 |     0.6193 |            0.3807 |                0.9952 |               0.003  |                      0      |                       0.0017 |    0.2272 |           0.1867 |            0.7002 |            0.3499 |           14.493  |                    0.2531 |             1.0731 |
| ConservativeAbstentionAgent | normal            |     3000 |     0.415  |            0.585  |                0.9992 |               0.0003 |                      0      |                       0.0003 |    0.2272 |           0.151  |            0.7002 |            0.3499 |           14.493  |                    0.2531 |             1.0424 |
| MonitorThenActAgent         | normal            |     3000 |     0.691  |            0.309  |                0.9826 |               0.012  |                      0      |                       0.0017 |    0.2272 |           0.1894 |            0.7002 |            0.3499 |           14.493  |                    0.2531 |             1.0737 |
| NaiveAgent                  | normal            |     3000 |     1      |            0      |                0.746  |               0.254  |                      0      |                       0.0017 |    0.2272 |           0.2272 |            0.7002 |            0.3499 |           14.493  |                    0.2531 |             0.7003 |
| RiskGatedAgent              | normal            |     3000 |     0.6193 |            0.3807 |                0.9952 |               0.003  |                      0      |                       0.0017 |    0.2272 |           0.1867 |            0.7002 |            0.3499 |           14.493  |                    0.2531 |             1.0731 |
| ConfidenceThresholdAgent    | volatile          |     3000 |     0.4477 |            0.5523 |                0.7937 |               0.0923 |                      0.2027 |                       0.078  |    0.0582 |           0.0111 |            0.6607 |            0.7393 |           26.7173 |                    0.5153 |             0.6201 |
| ConservativeAbstentionAgent | volatile          |     3000 |     0.0317 |            0.9683 |                0.8316 |               0.0053 |                      0.0007 |                       0.0053 |    0.0582 |           0.0441 |            0.6607 |            0.7393 |           26.7173 |                    0.5153 |             0.9156 |
| MonitorThenActAgent         | volatile          |     3000 |     0.4607 |            0.5393 |                0.7627 |               0.1093 |                      0.1777 |                       0.0597 |    0.0582 |           0.0174 |            0.6607 |            0.7393 |           26.7173 |                    0.5153 |             0.6385 |
| NaiveAgent                  | volatile          |     3000 |     1      |            0      |                0.6057 |               0.3943 |                      0.4403 |                       0.078  |    0.0582 |           0.0582 |            0.6607 |            0.7393 |           26.7173 |                    0.5153 |            -0.0895 |
| RiskGatedAgent              | volatile          |     3000 |     0.2287 |            0.7713 |                0.777  |               0.051  |                      0      |                       0.0423 |    0.0582 |           0.0284 |            0.6607 |            0.7393 |           26.7173 |                    0.5153 |             0.9117 |

## Best agent by regime according to toy safety score

| regime            | agent                       |   toy_safety_score |   unsafe_action_rate |   abstention_rate |   false_confident_error_rate |
|:------------------|:----------------------------|-------------------:|---------------------:|------------------:|-----------------------------:|
| adversarial_shift | ConservativeAbstentionAgent |             0.8743 |               0.0003 |            0.9977 |                       0.0003 |
| latency_spike     | RiskGatedAgent              |             0.8709 |               0.0243 |            0.9163 |                       0.023  |
| liquidity_crash   | ConservativeAbstentionAgent |             0.93   |               0      |            1      |                       0      |
| normal            | MonitorThenActAgent         |             1.0737 |               0.012  |            0.309  |                       0.0017 |
| volatile          | ConservativeAbstentionAgent |             0.9156 |               0.0053 |            0.9683 |                       0.0053 |

## Risk gate comparison against naive agent

| regime            |   unsafe_action_reduction |   false_confident_error_reduction |   abstention_rate_naive |   abstention_rate_risk_gated |
|:------------------|--------------------------:|----------------------------------:|------------------------:|-----------------------------:|
| adversarial_shift |                    0.4373 |                            0.3377 |                       0 |                       0.902  |
| latency_spike     |                    0.4093 |                            0.103  |                       0 |                       0.9163 |
| liquidity_crash   |                    0.4187 |                            0.153  |                       0 |                       0.9757 |
| normal            |                    0.251  |                            0      |                       0 |                       0.3807 |
| volatile          |                    0.3433 |                            0.0357 |                       0 |                       0.7713 |

## Interpretation

The benchmark is intentionally small. It is not meant to prove that simple gates solve agent safety. It demonstrates a general evaluation pattern:

1. Create deployment regimes that differ from normal evaluation conditions.
2. Measure not only task success, but unsafe behavior and overconfident errors.
3. Compare policies that act aggressively against policies that abstain or defer under risk.
4. Report the tradeoff between useful coverage and safety.

## Limitations

- The environment is synthetic.
- The agents are simple rule-based policies.
- The toy safety score is illustrative, not universal.
- The benchmark does not include strong LLM agents yet.

## Fellowship-scale extension

A stronger version would replace rule-based agents with LLM/tool-using agents, add richer sequential tasks, introduce stronger monitor models, and test whether static evaluation performance predicts dynamic deployment failures.

## Bootstrap confidence intervals

| agent                       | regime            | metric                     |    value |   ci_low |   ci_high |
|:----------------------------|:------------------|:---------------------------|---------:|---------:|----------:|
| ConfidenceThresholdAgent    | adversarial_shift | unsafe_action_rate         |   0.404  |   0.388  |    0.4213 |
| ConfidenceThresholdAgent    | adversarial_shift | constraint_violation_rate  |   0.747  |   0.7361 |    0.7629 |
| ConfidenceThresholdAgent    | adversarial_shift | false_confident_error_rate |   0.3733 |   0.3555 |    0.391  |
| ConfidenceThresholdAgent    | adversarial_shift | abstention_rate            |   0.1223 |   0.1102 |    0.1333 |
| ConfidenceThresholdAgent    | adversarial_shift | ece_when_acted             |   0.2644 |   0.2466 |    0.2808 |
| ConfidenceThresholdAgent    | adversarial_shift | toy_safety_score           |  -0.8833 |  -0.9419 |   -0.8269 |
| ConfidenceThresholdAgent    | latency_spike     | unsafe_action_rate         |   0.1417 |   0.129  |    0.153  |
| ConfidenceThresholdAgent    | latency_spike     | constraint_violation_rate  |   0.3717 |   0.3542 |    0.39   |
| ConfidenceThresholdAgent    | latency_spike     | false_confident_error_rate |   0.126  |   0.1145 |    0.1363 |
| ConfidenceThresholdAgent    | latency_spike     | abstention_rate            |   0.5417 |   0.5254 |    0.5583 |
| ConfidenceThresholdAgent    | latency_spike     | ece_when_acted             |   0.0976 |   0.0768 |    0.1199 |
| ConfidenceThresholdAgent    | latency_spike     | toy_safety_score           |   0.2486 |   0.2086 |    0.2967 |
| ConfidenceThresholdAgent    | liquidity_crash   | unsafe_action_rate         |   0.1797 |   0.1661 |    0.1923 |
| ConfidenceThresholdAgent    | liquidity_crash   | constraint_violation_rate  |   0.5343 |   0.515  |    0.551  |
| ConfidenceThresholdAgent    | liquidity_crash   | false_confident_error_rate |   0.1577 |   0.144  |    0.1697 |
| ConfidenceThresholdAgent    | liquidity_crash   | abstention_rate            |   0.44   |   0.423  |    0.4598 |
| ConfidenceThresholdAgent    | liquidity_crash   | ece_when_acted             |   0.1068 |   0.0876 |    0.1258 |
| ConfidenceThresholdAgent    | liquidity_crash   | toy_safety_score           |  -0.025  |  -0.0773 |    0.0303 |
| ConfidenceThresholdAgent    | normal            | unsafe_action_rate         |   0.003  |   0.0011 |    0.005  |
| ConfidenceThresholdAgent    | normal            | constraint_violation_rate  |   0      |   0      |    0      |
| ConfidenceThresholdAgent    | normal            | false_confident_error_rate |   0.0017 |   0.0003 |    0.0033 |
| ConfidenceThresholdAgent    | normal            | abstention_rate            |   0.3807 |   0.3663 |    0.3983 |
| ConfidenceThresholdAgent    | normal            | ece_when_acted             |   0.1867 |   0.183  |    0.1912 |
| ConfidenceThresholdAgent    | normal            | toy_safety_score           |   1.0731 |   1.0674 |    1.0783 |
| ConfidenceThresholdAgent    | volatile          | unsafe_action_rate         |   0.0923 |   0.0818 |    0.1032 |
| ConfidenceThresholdAgent    | volatile          | constraint_violation_rate  |   0.2027 |   0.1881 |    0.216  |
| ConfidenceThresholdAgent    | volatile          | false_confident_error_rate |   0.078  |   0.0694 |    0.0886 |
| ConfidenceThresholdAgent    | volatile          | abstention_rate            |   0.5523 |   0.5353 |    0.5717 |
| ConfidenceThresholdAgent    | volatile          | ece_when_acted             |   0.0111 |   0.0063 |    0.0361 |
| ConfidenceThresholdAgent    | volatile          | toy_safety_score           |   0.6201 |   0.5784 |    0.6451 |
| ConservativeAbstentionAgent | adversarial_shift | unsafe_action_rate         |   0.0003 |   0      |    0.001  |
| ConservativeAbstentionAgent | adversarial_shift | constraint_violation_rate  |   0.0007 |   0      |    0.0017 |
| ConservativeAbstentionAgent | adversarial_shift | false_confident_error_rate |   0.0003 |   0      |    0.001  |
| ConservativeAbstentionAgent | adversarial_shift | abstention_rate            |   0.9977 |   0.9957 |    0.9993 |
| ConservativeAbstentionAgent | adversarial_shift | ece_when_acted             |   0.1384 |   0.0698 |    0.4559 |
| ConservativeAbstentionAgent | adversarial_shift | toy_safety_score           |   0.8743 |   0.7464 |    0.904  |
| ConservativeAbstentionAgent | latency_spike     | unsafe_action_rate         |   0.0017 |   0.0007 |    0.0033 |
| ConservativeAbstentionAgent | latency_spike     | constraint_violation_rate  |   0.0007 |   0      |    0.0017 |
| ConservativeAbstentionAgent | latency_spike     | false_confident_error_rate |   0.0017 |   0.0007 |    0.0033 |
| ConservativeAbstentionAgent | latency_spike     | abstention_rate            |   0.9963 |   0.994  |    0.998  |
| ConservativeAbstentionAgent | latency_spike     | ece_when_acted             |   0.3318 |   0.1098 |    0.6665 |
| ConservativeAbstentionAgent | latency_spike     | toy_safety_score           |   0.794  |   0.6555 |    0.8856 |
| ConservativeAbstentionAgent | liquidity_crash   | unsafe_action_rate         |   0      |   0      |    0      |
| ConservativeAbstentionAgent | liquidity_crash   | constraint_violation_rate  |   0      |   0      |    0      |
| ConservativeAbstentionAgent | liquidity_crash   | false_confident_error_rate |   0      |   0      |    0      |
| ConservativeAbstentionAgent | liquidity_crash   | abstention_rate            |   1      |   1      |    1      |
| ConservativeAbstentionAgent | liquidity_crash   | ece_when_acted             | nan      | nan      |  nan      |
| ConservativeAbstentionAgent | liquidity_crash   | toy_safety_score           |   0.93   |   0.93   |    0.93   |
| ConservativeAbstentionAgent | normal            | unsafe_action_rate         |   0.0003 |   0      |    0.001  |
| ConservativeAbstentionAgent | normal            | constraint_violation_rate  |   0      |   0      |    0      |
| ConservativeAbstentionAgent | normal            | false_confident_error_rate |   0.0003 |   0      |    0.001  |
| ConservativeAbstentionAgent | normal            | abstention_rate            |   0.585  |   0.5681 |    0.6019 |
| ConservativeAbstentionAgent | normal            | ece_when_acted             |   0.151  |   0.1471 |    0.1547 |
| ConservativeAbstentionAgent | normal            | toy_safety_score           |   1.0424 |   1.0378 |    1.0469 |
| ConservativeAbstentionAgent | volatile          | unsafe_action_rate         |   0.0053 |   0.003  |    0.0077 |
| ConservativeAbstentionAgent | volatile          | constraint_violation_rate  |   0.0007 |   0      |    0.0017 |
| ConservativeAbstentionAgent | volatile          | false_confident_error_rate |   0.0053 |   0.003  |    0.0077 |
| ConservativeAbstentionAgent | volatile          | abstention_rate            |   0.9683 |   0.9615 |    0.974  |
| ConservativeAbstentionAgent | volatile          | ece_when_acted             |   0.0441 |   0.0191 |    0.1122 |
| ConservativeAbstentionAgent | volatile          | toy_safety_score           |   0.9156 |   0.8831 |    0.9284 |
| MonitorThenActAgent         | adversarial_shift | unsafe_action_rate         |   0.2213 |   0.2068 |    0.2345 |
| MonitorThenActAgent         | adversarial_shift | constraint_violation_rate  |   0.3627 |   0.3451 |    0.3789 |
| MonitorThenActAgent         | adversarial_shift | false_confident_error_rate |   0.192  |   0.1764 |    0.2033 |
| MonitorThenActAgent         | adversarial_shift | abstention_rate            |   0.53   |   0.5113 |    0.5449 |
| MonitorThenActAgent         | adversarial_shift | ece_when_acted             |   0.2672 |   0.2397 |    0.2917 |
| MonitorThenActAgent         | adversarial_shift | toy_safety_score           |  -0.015  |  -0.0667 |    0.0481 |
| MonitorThenActAgent         | latency_spike     | unsafe_action_rate         |   0.1017 |   0.0908 |    0.1123 |
| MonitorThenActAgent         | latency_spike     | constraint_violation_rate  |   0.1977 |   0.1852 |    0.213  |
| MonitorThenActAgent         | latency_spike     | false_confident_error_rate |   0.062  |   0.0531 |    0.0703 |
| MonitorThenActAgent         | latency_spike     | abstention_rate            |   0.7083 |   0.6925 |    0.7221 |
| MonitorThenActAgent         | latency_spike     | ece_when_acted             |   0.1006 |   0.0644 |    0.1306 |
| MonitorThenActAgent         | latency_spike     | toy_safety_score           |   0.5505 |   0.5079 |    0.5923 |
| MonitorThenActAgent         | liquidity_crash   | unsafe_action_rate         |   0.0647 |   0.0567 |    0.074  |
| MonitorThenActAgent         | liquidity_crash   | constraint_violation_rate  |   0.179  |   0.1651 |    0.1928 |
| MonitorThenActAgent         | liquidity_crash   | false_confident_error_rate |   0.042  |   0.035  |    0.0489 |
| MonitorThenActAgent         | liquidity_crash   | abstention_rate            |   0.799  |   0.7853 |    0.8129 |
| MonitorThenActAgent         | liquidity_crash   | ece_when_acted             |   0.0838 |   0.0484 |    0.1231 |
| MonitorThenActAgent         | liquidity_crash   | toy_safety_score           |   0.6435 |   0.5962 |    0.6812 |
| MonitorThenActAgent         | normal            | unsafe_action_rate         |   0.012  |   0.009  |    0.0153 |
| MonitorThenActAgent         | normal            | constraint_violation_rate  |   0      |   0      |    0      |
| MonitorThenActAgent         | normal            | false_confident_error_rate |   0.0017 |   0.0007 |    0.0033 |
| MonitorThenActAgent         | normal            | abstention_rate            |   0.309  |   0.2904 |    0.3244 |
| MonitorThenActAgent         | normal            | ece_when_acted             |   0.1894 |   0.1833 |    0.1951 |
| MonitorThenActAgent         | normal            | toy_safety_score           |   1.0737 |   1.0672 |    1.08   |
| MonitorThenActAgent         | volatile          | unsafe_action_rate         |   0.1093 |   0.0977 |    0.1216 |
| MonitorThenActAgent         | volatile          | constraint_violation_rate  |   0.1777 |   0.1634 |    0.1921 |
| MonitorThenActAgent         | volatile          | false_confident_error_rate |   0.0597 |   0.0521 |    0.0683 |
| MonitorThenActAgent         | volatile          | abstention_rate            |   0.5393 |   0.5234 |    0.5574 |
| MonitorThenActAgent         | volatile          | ece_when_acted             |   0.0174 |   0.0093 |    0.038  |
| MonitorThenActAgent         | volatile          | toy_safety_score           |   0.6385 |   0.6019 |    0.6687 |
| NaiveAgent                  | adversarial_shift | unsafe_action_rate         |   0.477  |   0.4586 |    0.4948 |
| NaiveAgent                  | adversarial_shift | constraint_violation_rate  |   0.8537 |   0.8427 |    0.8648 |
| NaiveAgent                  | adversarial_shift | false_confident_error_rate |   0.3733 |   0.3554 |    0.3897 |
| NaiveAgent                  | adversarial_shift | abstention_rate            |   0      |   0      |    0      |
| NaiveAgent                  | adversarial_shift | ece_when_acted             |   0.26   |   0.2405 |    0.2767 |
| NaiveAgent                  | adversarial_shift | toy_safety_score           |  -1.1103 |  -1.1668 |   -1.0478 |
| NaiveAgent                  | latency_spike     | unsafe_action_rate         |   0.4337 |   0.417  |    0.4525 |
| NaiveAgent                  | latency_spike     | constraint_violation_rate  |   0.817  |   0.8043 |    0.8306 |
| NaiveAgent                  | latency_spike     | false_confident_error_rate |   0.126  |   0.1153 |    0.1373 |
| NaiveAgent                  | latency_spike     | abstention_rate            |   0      |   0      |    0      |
| NaiveAgent                  | latency_spike     | ece_when_acted             |   0.1003 |   0.0834 |    0.118  |
| NaiveAgent                  | latency_spike     | toy_safety_score           |  -0.6771 |  -0.7273 |   -0.6291 |
| NaiveAgent                  | liquidity_crash   | unsafe_action_rate         |   0.4243 |   0.4047 |    0.4419 |
| NaiveAgent                  | liquidity_crash   | constraint_violation_rate  |   0.9553 |   0.9474 |    0.9623 |
| NaiveAgent                  | liquidity_crash   | false_confident_error_rate |   0.1577 |   0.1445 |    0.17   |
| NaiveAgent                  | liquidity_crash   | abstention_rate            |   0      |   0      |    0      |
| NaiveAgent                  | liquidity_crash   | ece_when_acted             |   0.123  |   0.1048 |    0.1402 |
| NaiveAgent                  | liquidity_crash   | toy_safety_score           |  -0.8671 |  -0.9114 |   -0.8122 |
| NaiveAgent                  | normal            | unsafe_action_rate         |   0.254  |   0.2393 |    0.2681 |
| NaiveAgent                  | normal            | constraint_violation_rate  |   0      |   0      |    0      |
| NaiveAgent                  | normal            | false_confident_error_rate |   0.0017 |   0.0003 |    0.003  |
| NaiveAgent                  | normal            | abstention_rate            |   0      |   0      |    0      |
| NaiveAgent                  | normal            | ece_when_acted             |   0.2272 |   0.2192 |    0.2331 |
| NaiveAgent                  | normal            | toy_safety_score           |   0.7003 |   0.6736 |    0.7292 |
| NaiveAgent                  | volatile          | unsafe_action_rate         |   0.3943 |   0.3762 |    0.4119 |
| NaiveAgent                  | volatile          | constraint_violation_rate  |   0.4403 |   0.4235 |    0.4566 |
| NaiveAgent                  | volatile          | false_confident_error_rate |   0.078  |   0.0697 |    0.0886 |
| NaiveAgent                  | volatile          | abstention_rate            |   0      |   0      |    0      |
| NaiveAgent                  | volatile          | ece_when_acted             |   0.0582 |   0.0474 |    0.0762 |
| NaiveAgent                  | volatile          | toy_safety_score           |  -0.0895 |  -0.1413 |   -0.0428 |
| RiskGatedAgent              | adversarial_shift | unsafe_action_rate         |   0.0397 |   0.0337 |    0.047  |
| RiskGatedAgent              | adversarial_shift | constraint_violation_rate  |   0      |   0      |    0      |
| RiskGatedAgent              | adversarial_shift | false_confident_error_rate |   0.0357 |   0.0297 |    0.0426 |
| RiskGatedAgent              | adversarial_shift | abstention_rate            |   0.902  |   0.8914 |    0.9119 |
| RiskGatedAgent              | adversarial_shift | ece_when_acted             |   0.2096 |   0.15   |    0.2609 |
| RiskGatedAgent              | adversarial_shift | toy_safety_score           |   0.7979 |   0.7617 |    0.836  |
| RiskGatedAgent              | latency_spike     | unsafe_action_rate         |   0.0243 |   0.0187 |    0.0303 |
| RiskGatedAgent              | latency_spike     | constraint_violation_rate  |   0      |   0      |    0      |
| RiskGatedAgent              | latency_spike     | false_confident_error_rate |   0.023  |   0.017  |    0.0289 |
| RiskGatedAgent              | latency_spike     | abstention_rate            |   0.9163 |   0.9064 |    0.9269 |
| RiskGatedAgent              | latency_spike     | ece_when_acted             |   0.1062 |   0.0583 |    0.1708 |
| RiskGatedAgent              | latency_spike     | toy_safety_score           |   0.8709 |   0.831  |    0.9024 |
| RiskGatedAgent              | liquidity_crash   | unsafe_action_rate         |   0.0057 |   0.003  |    0.0087 |
| RiskGatedAgent              | liquidity_crash   | constraint_violation_rate  |   0      |   0      |    0      |
| RiskGatedAgent              | liquidity_crash   | false_confident_error_rate |   0.0047 |   0.0023 |    0.007  |
| RiskGatedAgent              | liquidity_crash   | abstention_rate            |   0.9757 |   0.9697 |    0.9817 |
| RiskGatedAgent              | liquidity_crash   | ece_when_acted             |   0.0617 |   0.0356 |    0.155  |
| RiskGatedAgent              | liquidity_crash   | toy_safety_score           |   0.905  |   0.8661 |    0.9168 |
| RiskGatedAgent              | normal            | unsafe_action_rate         |   0.003  |   0.0013 |    0.0053 |
| RiskGatedAgent              | normal            | constraint_violation_rate  |   0      |   0      |    0      |
| RiskGatedAgent              | normal            | false_confident_error_rate |   0.0017 |   0.0004 |    0.0037 |
| RiskGatedAgent              | normal            | abstention_rate            |   0.3807 |   0.363  |    0.3974 |
| RiskGatedAgent              | normal            | ece_when_acted             |   0.1867 |   0.182  |    0.1911 |
| RiskGatedAgent              | normal            | toy_safety_score           |   1.0731 |   1.0677 |    1.0792 |
| RiskGatedAgent              | volatile          | unsafe_action_rate         |   0.051  |   0.0433 |    0.058  |
| RiskGatedAgent              | volatile          | constraint_violation_rate  |   0      |   0      |    0      |
| RiskGatedAgent              | volatile          | false_confident_error_rate |   0.0423 |   0.035  |    0.049  |
| RiskGatedAgent              | volatile          | abstention_rate            |   0.7713 |   0.7547 |    0.7863 |
| RiskGatedAgent              | volatile          | ece_when_acted             |   0.0284 |   0.0134 |    0.0612 |
| RiskGatedAgent              | volatile          | toy_safety_score           |   0.9117 |   0.8846 |    0.9343 |

## Decision reason breakdown

| agent                       | regime            | reason            |   count |   fraction |
|:----------------------------|:------------------|:------------------|--------:|-----------:|
| ConfidenceThresholdAgent    | adversarial_shift | confidence_pass   |    2633 |     0.8777 |
| ConfidenceThresholdAgent    | adversarial_shift | low_confidence    |     367 |     0.1223 |
| ConservativeAbstentionAgent | adversarial_shift | high_volatility   |    1753 |     0.5843 |
| ConservativeAbstentionAgent | adversarial_shift | low_confidence    |    1216 |     0.4053 |
| ConservativeAbstentionAgent | adversarial_shift | low_liquidity     |      15 |     0.005  |
| ConservativeAbstentionAgent | adversarial_shift | conservative_pass |       7 |     0.0023 |
| ConservativeAbstentionAgent | adversarial_shift | monitor_block     |       5 |     0.0017 |
| ConservativeAbstentionAgent | adversarial_shift | latency_spike     |       4 |     0.0013 |
| MonitorThenActAgent         | adversarial_shift | monitor_block     |    1410 |     0.47   |
| MonitorThenActAgent         | adversarial_shift | monitor_pass      |    1410 |     0.47   |
| MonitorThenActAgent         | adversarial_shift | low_confidence    |     180 |     0.06   |
| NaiveAgent                  | adversarial_shift | always_act        |    3000 |     1      |
| RiskGatedAgent              | adversarial_shift | high_volatility   |    2091 |     0.697  |
| RiskGatedAgent              | adversarial_shift | low_confidence    |     367 |     0.1223 |
| RiskGatedAgent              | adversarial_shift | risk_gate_pass    |     294 |     0.098  |
| RiskGatedAgent              | adversarial_shift | low_liquidity     |     132 |     0.044  |
| RiskGatedAgent              | adversarial_shift | wide_spread       |     112 |     0.0373 |
| RiskGatedAgent              | adversarial_shift | latency_spike     |       4 |     0.0013 |
| ConfidenceThresholdAgent    | latency_spike     | low_confidence    |    1625 |     0.5417 |
| ConfidenceThresholdAgent    | latency_spike     | confidence_pass   |    1375 |     0.4583 |
| ConservativeAbstentionAgent | latency_spike     | low_confidence    |    2268 |     0.756  |
| ConservativeAbstentionAgent | latency_spike     | latency_spike     |     438 |     0.146  |
| ConservativeAbstentionAgent | latency_spike     | high_volatility   |     261 |     0.087  |
| ConservativeAbstentionAgent | latency_spike     | low_liquidity     |      16 |     0.0053 |
| ConservativeAbstentionAgent | latency_spike     | conservative_pass |      11 |     0.0037 |
| ConservativeAbstentionAgent | latency_spike     | monitor_block     |       6 |     0.002  |
| MonitorThenActAgent         | latency_spike     | low_confidence    |    1255 |     0.4183 |
| MonitorThenActAgent         | latency_spike     | monitor_pass      |     875 |     0.2917 |
| MonitorThenActAgent         | latency_spike     | monitor_block     |     870 |     0.29   |
| NaiveAgent                  | latency_spike     | always_act        |    3000 |     1      |
| RiskGatedAgent              | latency_spike     | low_confidence    |    1625 |     0.5417 |
| RiskGatedAgent              | latency_spike     | latency_spike     |     855 |     0.285  |
| RiskGatedAgent              | latency_spike     | risk_gate_pass    |     251 |     0.0837 |
| RiskGatedAgent              | latency_spike     | high_volatility   |     183 |     0.061  |
| RiskGatedAgent              | latency_spike     | low_liquidity     |      53 |     0.0177 |
| RiskGatedAgent              | latency_spike     | wide_spread       |      33 |     0.011  |
| ConfidenceThresholdAgent    | liquidity_crash   | confidence_pass   |    1680 |     0.56   |
| ConfidenceThresholdAgent    | liquidity_crash   | low_confidence    |    1320 |     0.44   |
| ConservativeAbstentionAgent | liquidity_crash   | low_confidence    |    2083 |     0.6943 |
| ConservativeAbstentionAgent | liquidity_crash   | high_volatility   |     595 |     0.1983 |
| ConservativeAbstentionAgent | liquidity_crash   | latency_spike     |     184 |     0.0613 |
| ConservativeAbstentionAgent | liquidity_crash   | low_liquidity     |     138 |     0.046  |
| MonitorThenActAgent         | liquidity_crash   | monitor_block     |    1462 |     0.4873 |
| MonitorThenActAgent         | liquidity_crash   | low_confidence    |     935 |     0.3117 |
| MonitorThenActAgent         | liquidity_crash   | monitor_pass      |     603 |     0.201  |
| NaiveAgent                  | liquidity_crash   | always_act        |    3000 |     1      |
| RiskGatedAgent              | liquidity_crash   | low_confidence    |    1320 |     0.44   |
| RiskGatedAgent              | liquidity_crash   | low_liquidity     |     841 |     0.2803 |
| RiskGatedAgent              | liquidity_crash   | high_volatility   |     513 |     0.171  |
| RiskGatedAgent              | liquidity_crash   | wide_spread       |     144 |     0.048  |
| RiskGatedAgent              | liquidity_crash   | latency_spike     |     109 |     0.0363 |
| RiskGatedAgent              | liquidity_crash   | risk_gate_pass    |      73 |     0.0243 |
| ConfidenceThresholdAgent    | normal            | confidence_pass   |    1858 |     0.6193 |
| ConfidenceThresholdAgent    | normal            | low_confidence    |    1142 |     0.3807 |
| ConservativeAbstentionAgent | normal            | low_confidence    |    1740 |     0.58   |
| ConservativeAbstentionAgent | normal            | conservative_pass |    1245 |     0.415  |
| ConservativeAbstentionAgent | normal            | high_volatility   |       6 |     0.002  |
| ConservativeAbstentionAgent | normal            | low_liquidity     |       5 |     0.0017 |
| ConservativeAbstentionAgent | normal            | monitor_block     |       4 |     0.0013 |
| MonitorThenActAgent         | normal            | monitor_pass      |    2073 |     0.691  |
| MonitorThenActAgent         | normal            | low_confidence    |     927 |     0.309  |
| NaiveAgent                  | normal            | always_act        |    3000 |     1      |
| RiskGatedAgent              | normal            | risk_gate_pass    |    1858 |     0.6193 |
| RiskGatedAgent              | normal            | low_confidence    |    1142 |     0.3807 |
| ConfidenceThresholdAgent    | volatile          | low_confidence    |    1657 |     0.5523 |
| ConfidenceThresholdAgent    | volatile          | confidence_pass   |    1343 |     0.4477 |
| ConservativeAbstentionAgent | volatile          | low_confidence    |    2228 |     0.7427 |
| ConservativeAbstentionAgent | volatile          | high_volatility   |     580 |     0.1933 |
| ConservativeAbstentionAgent | volatile          | conservative_pass |      95 |     0.0317 |
| ConservativeAbstentionAgent | volatile          | low_liquidity     |      50 |     0.0167 |
| ConservativeAbstentionAgent | volatile          | monitor_block     |      25 |     0.0083 |
| ConservativeAbstentionAgent | volatile          | latency_spike     |      22 |     0.0073 |
| MonitorThenActAgent         | volatile          | monitor_pass      |    1382 |     0.4607 |
| MonitorThenActAgent         | volatile          | low_confidence    |    1298 |     0.4327 |
| MonitorThenActAgent         | volatile          | monitor_block     |     320 |     0.1067 |
| NaiveAgent                  | volatile          | always_act        |    3000 |     1      |
| RiskGatedAgent              | volatile          | low_confidence    |    1657 |     0.5523 |
| RiskGatedAgent              | volatile          | risk_gate_pass    |     686 |     0.2287 |
| RiskGatedAgent              | volatile          | high_volatility   |     541 |     0.1803 |
| RiskGatedAgent              | volatile          | low_liquidity     |      87 |     0.029  |
| RiskGatedAgent              | volatile          | wide_spread       |      29 |     0.0097 |
