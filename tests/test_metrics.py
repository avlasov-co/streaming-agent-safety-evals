import pandas as pd

from src.agents import ACT_NEGATIVE, ACT_POSITIVE, ABSTAIN
from src.metrics import add_action_outcomes, expected_calibration_error, summarize


def test_false_confident_error_is_detected():
    df = pd.DataFrame(
        [
            {
                "agent": "TestAgent",
                "regime": "test",
                "action": ACT_POSITIVE,
                "true_direction": -1,
                "predicted_direction": 1,
                "confidence": 0.95,
                "unsafe_condition": False,
                "volatility": 0.1,
                "latency_ms": 1,
                "monitor_risk_score": 0.1,
            }
        ]
    )
    out = add_action_outcomes(df)
    assert bool(out.loc[0, "unsafe_action"])
    assert bool(out.loc[0, "false_confident_error"])


def test_abstention_is_not_counted_as_unsafe_action():
    df = pd.DataFrame(
        [
            {
                "agent": "TestAgent",
                "regime": "test",
                "action": ABSTAIN,
                "true_direction": -1,
                "predicted_direction": 1,
                "confidence": 0.95,
                "unsafe_condition": True,
                "volatility": 0.9,
                "latency_ms": 90,
                "monitor_risk_score": 0.9,
            }
        ]
    )
    summary = summarize(df)
    assert summary.loc[0, "coverage"] == 0.0
    assert summary.loc[0, "unsafe_action_rate"] == 0.0
    assert summary.loc[0, "constraint_violation_rate"] == 0.0


def test_expected_calibration_error_is_nonnegative():
    df = pd.DataFrame(
        {
            "confidence": [0.1, 0.8, 0.9],
            "prediction_correct": [False, True, False],
        }
    )
    assert expected_calibration_error(df) >= 0.0


def test_summary_uses_toy_safety_score_name():
    df = pd.DataFrame(
        [
            {
                "agent": "TestAgent",
                "regime": "test",
                "action": ACT_POSITIVE,
                "true_direction": 1,
                "predicted_direction": 1,
                "confidence": 0.9,
                "unsafe_condition": False,
                "volatility": 0.1,
                "latency_ms": 1,
                "monitor_risk_score": 0.1,
            }
        ]
    )
    summary = summarize(df)
    assert "toy_safety_score" in summary.columns
    legacy_name = "safety" + "_score"
    assert legacy_name not in summary.columns
