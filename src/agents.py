from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Deque, Dict, Protocol

import pandas as pd


ACT_POSITIVE = "ACT_POSITIVE"
ACT_NEGATIVE = "ACT_NEGATIVE"
ABSTAIN = "ABSTAIN"
ASK_OVERSIGHT = "ASK_OVERSIGHT"


class Agent(Protocol):
    name: str

    def decide(self, row: pd.Series) -> Dict[str, str]:
        ...


def _direction_action(row: pd.Series) -> str:
    return ACT_POSITIVE if int(row["predicted_direction"]) == 1 else ACT_NEGATIVE


def _risk_feature_count(
    row: pd.Series,
    *,
    volatility_limit: float,
    latency_limit_ms: float,
    liquidity_floor: float,
    spread_limit: float,
    monitor_risk_limit: float,
) -> int:
    """Count independent high-risk signals on a single event."""
    return sum(
        [
            float(row["volatility"]) > volatility_limit,
            float(row["latency_ms"]) > latency_limit_ms,
            float(row["liquidity"]) < liquidity_floor,
            float(row["spread"]) > spread_limit,
            float(row["monitor_risk_score"]) > monitor_risk_limit,
        ]
    )


@dataclass
class NaiveAgent:
    name: str = "NaiveAgent"

    def decide(self, row: pd.Series) -> Dict[str, str]:
        return {"action": _direction_action(row), "reason": "always_act"}


@dataclass
class ConfidenceThresholdAgent:
    threshold: float = 0.68
    name: str = "ConfidenceThresholdAgent"

    def decide(self, row: pd.Series) -> Dict[str, str]:
        if float(row["confidence"]) < self.threshold:
            return {"action": ABSTAIN, "reason": "low_confidence"}
        return {"action": _direction_action(row), "reason": "confidence_pass"}


@dataclass
class RiskGatedAgent:
    confidence_threshold: float = 0.68
    volatility_limit: float = 0.78
    latency_limit_ms: float = 70.0
    liquidity_floor: float = 0.25
    spread_limit: float = 0.10
    name: str = "RiskGatedAgent"

    def decide(self, row: pd.Series) -> Dict[str, str]:
        if float(row["confidence"]) < self.confidence_threshold:
            return {"action": ABSTAIN, "reason": "low_confidence"}
        if float(row["volatility"]) > self.volatility_limit:
            return {"action": ABSTAIN, "reason": "high_volatility"}
        if float(row["latency_ms"]) > self.latency_limit_ms:
            return {"action": ABSTAIN, "reason": "latency_spike"}
        if float(row["liquidity"]) < self.liquidity_floor:
            return {"action": ABSTAIN, "reason": "low_liquidity"}
        if float(row["spread"]) > self.spread_limit:
            return {"action": ABSTAIN, "reason": "wide_spread"}
        return {"action": _direction_action(row), "reason": "risk_gate_pass"}


@dataclass
class MonitorThenActAgent:
    confidence_threshold: float = 0.64
    monitor_risk_limit: float = 0.62
    name: str = "MonitorThenActAgent"

    def decide(self, row: pd.Series) -> Dict[str, str]:
        if float(row["confidence"]) < self.confidence_threshold:
            return {"action": ABSTAIN, "reason": "low_confidence"}
        if float(row["monitor_risk_score"]) > self.monitor_risk_limit:
            return {"action": ABSTAIN, "reason": "monitor_block"}
        return {"action": _direction_action(row), "reason": "monitor_pass"}


@dataclass
class ConservativeAbstentionAgent:
    confidence_threshold: float = 0.76
    volatility_limit: float = 0.65
    latency_limit_ms: float = 45.0
    liquidity_floor: float = 0.40
    monitor_risk_limit: float = 0.50
    name: str = "ConservativeAbstentionAgent"

    def decide(self, row: pd.Series) -> Dict[str, str]:
        checks = {
            "low_confidence": float(row["confidence"]) < self.confidence_threshold,
            "high_volatility": float(row["volatility"]) > self.volatility_limit,
            "latency_spike": float(row["latency_ms"]) > self.latency_limit_ms,
            "low_liquidity": float(row["liquidity"]) < self.liquidity_floor,
            "monitor_block": float(row["monitor_risk_score"]) > self.monitor_risk_limit,
        }
        for reason, failed in checks.items():
            if failed:
                return {"action": ABSTAIN, "reason": reason}
        return {"action": _direction_action(row), "reason": "conservative_pass"}


@dataclass
class OversightSeekingAgent:
    """Escalate when independent risk signals suggest action is unsafe.

    Unlike abstention-only policies, this agent exposes a separate
    `ASK_OVERSIGHT` action. That lets the episode evaluator distinguish
    useful escalation from simple refusal and measure whether the agent asks
    for help when an avoidable failure is likely.
    """

    confidence_threshold: float = 0.66
    oversight_confidence_threshold: float = 0.60
    volatility_limit: float = 0.78
    latency_limit_ms: float = 70.0
    liquidity_floor: float = 0.25
    spread_limit: float = 0.10
    monitor_risk_limit: float = 0.62
    risk_signal_count_for_oversight: int = 2
    name: str = "OversightSeekingAgent"

    def decide(self, row: pd.Series) -> Dict[str, str]:
        risk_signals = _risk_feature_count(
            row,
            volatility_limit=self.volatility_limit,
            latency_limit_ms=self.latency_limit_ms,
            liquidity_floor=self.liquidity_floor,
            spread_limit=self.spread_limit,
            monitor_risk_limit=self.monitor_risk_limit,
        )
        confidence = float(row["confidence"])
        if risk_signals >= self.risk_signal_count_for_oversight:
            return {"action": ASK_OVERSIGHT, "reason": "multiple_risk_signals"}
        if float(row["monitor_risk_score"]) > self.monitor_risk_limit and confidence < self.confidence_threshold:
            return {"action": ASK_OVERSIGHT, "reason": "monitor_risk_with_weak_confidence"}
        if confidence < self.oversight_confidence_threshold:
            return {"action": ABSTAIN, "reason": "low_confidence"}
        return {"action": _direction_action(row), "reason": "oversight_not_needed"}


@dataclass
class DriftDetector:
    """Small moving-window detector for regime-shift-like risk changes."""

    window_size: int = 8
    volatility_limit: float = 0.70
    latency_limit_ms: float = 55.0
    liquidity_floor: float = 0.35
    spread_limit: float = 0.085
    monitor_risk_limit: float = 0.55
    min_signals_for_suspected_shift: int = 2
    min_signals_for_confirmed_shift: int = 3
    _window: Deque[dict[str, float]] = field(default_factory=deque, init=False, repr=False)

    def reset(self) -> None:
        self._window.clear()

    def update(self, row: pd.Series) -> Dict[str, object]:
        self._window.append(
            {
                "volatility": float(row["volatility"]),
                "latency_ms": float(row["latency_ms"]),
                "liquidity": float(row["liquidity"]),
                "spread": float(row["spread"]),
                "monitor_risk_score": float(row["monitor_risk_score"]),
            }
        )
        while len(self._window) > self.window_size:
            self._window.popleft()

        means = {
            key: sum(item[key] for item in self._window) / len(self._window)
            for key in self._window[0]
        }
        signals = {
            "high_volatility": means["volatility"] > self.volatility_limit,
            "latency_spike": means["latency_ms"] > self.latency_limit_ms,
            "low_liquidity": means["liquidity"] < self.liquidity_floor,
            "wide_spread": means["spread"] > self.spread_limit,
            "monitor_risk": means["monitor_risk_score"] > self.monitor_risk_limit,
        }
        signal_count = sum(signals.values())
        confirmed = signal_count >= self.min_signals_for_confirmed_shift
        suspected = confirmed or signal_count >= self.min_signals_for_suspected_shift
        return {
            "suspected_shift": suspected,
            "confirmed_shift": confirmed,
            "signal_count": signal_count,
            "signals": signals,
            "means": means,
        }


@dataclass
class ShiftAwareRiskAgent:
    """Risk-gated policy that tightens behavior after detected drift."""

    confidence_threshold: float = 0.68
    tightened_confidence_threshold: float = 0.74
    volatility_limit: float = 0.78
    tightened_volatility_limit: float = 0.66
    latency_limit_ms: float = 70.0
    tightened_latency_limit_ms: float = 55.0
    liquidity_floor: float = 0.25
    tightened_liquidity_floor: float = 0.35
    spread_limit: float = 0.10
    tightened_spread_limit: float = 0.075
    monitor_risk_limit: float = 0.62
    tightened_monitor_risk_limit: float = 0.52
    detector: DriftDetector = field(default_factory=DriftDetector)
    name: str = "ShiftAwareRiskAgent"

    def reset(self) -> None:
        self.detector.reset()

    def decide(self, row: pd.Series) -> Dict[str, str]:
        drift_state = self.detector.update(row)
        confirmed_shift = bool(drift_state["confirmed_shift"])
        suspected_shift = bool(drift_state["suspected_shift"])

        confidence_threshold = self.tightened_confidence_threshold if suspected_shift else self.confidence_threshold
        volatility_limit = self.tightened_volatility_limit if suspected_shift else self.volatility_limit
        latency_limit_ms = self.tightened_latency_limit_ms if suspected_shift else self.latency_limit_ms
        liquidity_floor = self.tightened_liquidity_floor if suspected_shift else self.liquidity_floor
        spread_limit = self.tightened_spread_limit if suspected_shift else self.spread_limit
        monitor_risk_limit = self.tightened_monitor_risk_limit if suspected_shift else self.monitor_risk_limit

        risk_signals = _risk_feature_count(
            row,
            volatility_limit=volatility_limit,
            latency_limit_ms=latency_limit_ms,
            liquidity_floor=liquidity_floor,
            spread_limit=spread_limit,
            monitor_risk_limit=monitor_risk_limit,
        )
        if confirmed_shift and risk_signals >= 1:
            return {"action": ASK_OVERSIGHT, "reason": "confirmed_shift_oversight"}
        if suspected_shift and risk_signals >= 2:
            return {"action": ASK_OVERSIGHT, "reason": "suspected_shift_multiple_risks"}
        if float(row["confidence"]) < confidence_threshold:
            return {"action": ABSTAIN, "reason": "shift_tightened_low_confidence" if suspected_shift else "low_confidence"}
        if risk_signals:
            return {"action": ABSTAIN, "reason": "shift_tightened_risk_gate" if suspected_shift else "risk_gate_block"}
        return {"action": _direction_action(row), "reason": "shift_aware_pass"}


def default_agents() -> list[Agent]:
    return [
        NaiveAgent(),
        ConfidenceThresholdAgent(),
        RiskGatedAgent(),
        MonitorThenActAgent(),
        ConservativeAbstentionAgent(),
        OversightSeekingAgent(),
        ShiftAwareRiskAgent(),
    ]
