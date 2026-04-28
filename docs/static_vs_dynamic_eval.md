# Static vs Dynamic Evaluation

Many machine‑learning benchmarks evaluate a model’s predictions on a fixed test set.  The model sees an input once, produces an output and is scored against the ground truth.  This approach is called **static evaluation**.  While static accuracy is important, it tells us little about how a system behaves when deployed as an agent that acts repeatedly under changing conditions.

## Static evaluation

In static evaluation, the data distribution is assumed to match the training distribution.  The model’s predictions are treated independently; there is no notion of feedback or risk.  Accuracy, precision, recall and other standard metrics quantify how often predictions match labels.  Static evaluation is simple to compute and widely used in machine learning.

However, static evaluation has blind spots when we consider safety:

* It does not measure **decision quality**.  A model might be wrong 30% of the time, but if those errors correspond to high‑risk actions, the deployed agent could be unsafe.
* It does not capture **confidence drift**.  A model may output over‑confident scores in regions of the input space not seen during training, leading an agent to act incorrectly with high confidence.
* It ignores **distribution shift**.  In the real world, the environment changes.  Data may become noisier, more volatile or adversarial.  A model with high static accuracy can fail catastrophically under shift.

## Dynamic evaluation

Dynamic evaluation refers to testing an agent in a deployment‑like setting where it receives a stream of observations, makes decisions over time and interacts with a changing environment.  Key features of dynamic evaluation include:

* **Sequential decisions**: The agent acts repeatedly, so errors can accumulate or compound.
* **Changing conditions**: The environment may shift between regimes (normal, volatile, adversarial) with different risk profiles.
* **Uncertainty and feedback**: The agent must decide whether to act, abstain or seek oversight based on incomplete information and confidence scores.
* **Safety metrics**: Measures such as unsafe action rate and constraint violation rate quantify harmful behaviour directly, rather than relying on accuracy alone.

Dynamic evaluations are more complex to implement but provide insights into safety that static tests miss.  For example, a model might achieve 80% accuracy on a static test but, when deployed, act incorrectly 50% of the time under a new regime because it continues to trust its confidence scores.

## How this benchmark demonstrates the gap

The streaming agent safety benchmark illustrates the difference between static and dynamic evaluation.  The **NaiveAgent** and **ConfidenceThresholdAgent** may perform similarly under the normal regime (static evaluation), but their unsafe action rates diverge sharply when the environment shifts.  In adversarial and latency‑spike regimes, the **NaiveAgent** acts confidently but incorrectly, while the **RiskGatedAgent** abstains during risky conditions.  These differences are invisible if we only look at overall accuracy on the normal regime.

To quantify this gap, you can run the provided `src/static_vs_dynamic.py` script to compute metrics for a “static” evaluation (normal regime only) versus a “dynamic” evaluation (all regimes combined).  The script outputs `results/static_vs_dynamic.csv` and `figures/static_vs_dynamic_gap.png` showing how normal-regime metrics diverge from dynamic all-regime behaviour.  Dynamic evaluations should therefore be part of any safety assessment for agentic systems.