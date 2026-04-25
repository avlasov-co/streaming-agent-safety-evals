from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Protocol

import pandas as pd


ACT_POSITIVE = "ACT_POSITIVE"
ACT_NEGATIVE = "ACT_NEGATIVE"
ABSTAIN = "ABSTAIN"


class Agent(Protocol):
    name: str

    def decide(self, row: pd.Series) -> Dict[str, str]:
        ...


def _direction_action(row: pd.Series) -> str:
    return ACT_POSITIVE if int(row["predicted_direction"]) == 1 else ACT_NEGATIVE


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


def default_agents() -> list[Agent]:
    return [
        NaiveAgent(),
        ConfidenceThresholdAgent(),
        RiskGatedAgent(),
        MonitorThenActAgent(),
        ConservativeAbstentionAgent(),
    ]
