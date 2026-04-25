from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Iterable, List

import numpy as np
import pandas as pd


REGIMES = ["normal", "volatile", "adversarial_shift", "latency_spike", "liquidity_crash"]


@dataclass(frozen=True)
class RegimeConfig:
    correctness_prob: float
    confidence_correct_mean: float
    confidence_wrong_mean: float
    confidence_std: float
    volatility_mean: float
    volatility_std: float
    latency_mean: float
    latency_std: float
    liquidity_mean: float
    liquidity_std: float
    spread_mean: float
    spread_std: float
    drift_strength: float


REGIME_CONFIGS: Dict[str, RegimeConfig] = {
    "normal": RegimeConfig(
        correctness_prob=0.74,
        confidence_correct_mean=0.78,
        confidence_wrong_mean=0.48,
        confidence_std=0.10,
        volatility_mean=0.32,
        volatility_std=0.12,
        latency_mean=12,
        latency_std=5,
        liquidity_mean=0.75,
        liquidity_std=0.12,
        spread_mean=0.025,
        spread_std=0.010,
        drift_strength=0.04,
    ),
    "volatile": RegimeConfig(
        correctness_prob=0.62,
        confidence_correct_mean=0.72,
        confidence_wrong_mean=0.58,
        confidence_std=0.14,
        volatility_mean=0.72,
        volatility_std=0.15,
        latency_mean=25,
        latency_std=12,
        liquidity_mean=0.50,
        liquidity_std=0.18,
        spread_mean=0.055,
        spread_std=0.025,
        drift_strength=0.12,
    ),
    "adversarial_shift": RegimeConfig(
        correctness_prob=0.52,
        confidence_correct_mean=0.80,
        confidence_wrong_mean=0.77,
        confidence_std=0.09,
        volatility_mean=0.84,
        volatility_std=0.10,
        latency_mean=30,
        latency_std=15,
        liquidity_mean=0.40,
        liquidity_std=0.18,
        spread_mean=0.075,
        spread_std=0.030,
        drift_strength=0.20,
    ),
    "latency_spike": RegimeConfig(
        correctness_prob=0.58,
        confidence_correct_mean=0.70,
        confidence_wrong_mean=0.63,
        confidence_std=0.13,
        volatility_mean=0.58,
        volatility_std=0.16,
        latency_mean=85,
        latency_std=30,
        liquidity_mean=0.46,
        liquidity_std=0.20,
        spread_mean=0.065,
        spread_std=0.028,
        drift_strength=0.13,
    ),
    "liquidity_crash": RegimeConfig(
        correctness_prob=0.57,
        confidence_correct_mean=0.73,
        confidence_wrong_mean=0.66,
        confidence_std=0.12,
        volatility_mean=0.67,
        volatility_std=0.15,
        latency_mean=45,
        latency_std=18,
        liquidity_mean=0.18,
        liquidity_std=0.10,
        spread_mean=0.115,
        spread_std=0.040,
        drift_strength=0.16,
    ),
}


def _clip01(x: np.ndarray | float) -> np.ndarray | float:
    return np.clip(x, 0.0, 1.0)


def _random_walk(n: int, rng: np.random.Generator, strength: float) -> np.ndarray:
    noise = rng.normal(0.0, strength, size=n)
    walk = np.cumsum(noise)
    walk = (walk - walk.mean()) / (walk.std() + 1e-8)
    return np.tanh(walk / 3.0)


def generate_regime_events(regime: str, n: int, rng: np.random.Generator, start_event_id: int = 0) -> pd.DataFrame:
    if regime not in REGIME_CONFIGS:
        raise ValueError(f"Unknown regime: {regime}. Expected one of {list(REGIME_CONFIGS)}")

    cfg = REGIME_CONFIGS[regime]
    drift = _random_walk(n=n, rng=rng, strength=cfg.drift_strength)

    true_direction = np.where(rng.normal(0.0, 1.0, size=n) + drift > 0, 1, -1)
    is_correct = rng.random(n) < cfg.correctness_prob
    predicted_direction = np.where(is_correct, true_direction, -true_direction)

    confidence_mean = np.where(is_correct, cfg.confidence_correct_mean, cfg.confidence_wrong_mean)
    confidence = _clip01(rng.normal(confidence_mean, cfg.confidence_std))

    volatility = _clip01(rng.normal(cfg.volatility_mean + 0.10 * np.abs(drift), cfg.volatility_std, size=n))
    latency_ms = np.maximum(1.0, rng.normal(cfg.latency_mean + 8 * np.abs(drift), cfg.latency_std, size=n))
    liquidity = _clip01(rng.normal(cfg.liquidity_mean - 0.08 * np.abs(drift), cfg.liquidity_std, size=n))
    spread = np.maximum(0.001, rng.normal(cfg.spread_mean + 0.012 * np.abs(drift), cfg.spread_std, size=n))
    order_imbalance = _clip01(rng.normal(0.5 + 0.18 * predicted_direction + 0.08 * drift, 0.22, size=n)) * 2 - 1

    unsafe_condition = (
        (volatility > 0.80)
        | (latency_ms > 70)
        | (liquidity < 0.25)
        | (spread > 0.10)
    )

    # A separate monitor score that is imperfect but useful.
    monitor_risk_score = _clip01(
        0.35 * volatility
        + 0.25 * _clip01(latency_ms / 100.0)
        + 0.25 * (1.0 - liquidity)
        + 0.15 * _clip01(spread / 0.15)
        + rng.normal(0.0, 0.08, size=n)
    )

    return pd.DataFrame(
        {
            "event_id": np.arange(start_event_id, start_event_id + n),
            "timestep": np.arange(n),
            "regime": regime,
            "true_direction": true_direction,
            "predicted_direction": predicted_direction,
            "confidence": confidence,
            "volatility": volatility,
            "latency_ms": latency_ms,
            "liquidity": liquidity,
            "spread": spread,
            "order_imbalance": order_imbalance,
            "drift": drift,
            "monitor_risk_score": monitor_risk_score,
            "unsafe_condition": unsafe_condition,
        }
    )


def generate_dataset(n_per_regime: int = 3000, seed: int = 42, regimes: Iterable[str] = REGIMES) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    frames: List[pd.DataFrame] = []
    event_id = 0

    for regime in regimes:
        df = generate_regime_events(regime=regime, n=n_per_regime, rng=rng, start_event_id=event_id)
        frames.append(df)
        event_id += n_per_regime

    return pd.concat(frames, ignore_index=True)
