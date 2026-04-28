"""
Utilities for running multi‑step episodes with risk accumulation.

This module provides helpers to simulate sequential decision episodes.  In a
multi‑step episode an agent repeatedly observes streaming events and makes
decisions until either the maximum number of steps is reached or the risk
budget is exhausted.  Unsafe or incorrect actions reduce the risk budget and
will eventually terminate the episode.  By comparing how long different
policies operate safely under various regimes we can evaluate their
robustness beyond one‑off accuracy metrics.

An episode starts with a fixed `risk_budget`.  Each time an agent makes an
incorrect prediction the budget is decreased by `incorrect_penalty`.  If the
agent acts under an unsafe condition the budget is decreased by
`unsafe_penalty`.  Abstentions leave the budget unchanged.  When the budget
falls to zero the episode is considered a failure and ends early.  The
episode returns whether a failure occurred and how many steps were taken.

These helpers do not perform any random training; they reuse the existing
synthetic data generator from ``src.simulate``.  Agents must conform to the
``Agent`` protocol from ``src.agents`` and should implement a ``decide``
method that returns an action and a reason.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Dict, Tuple

import numpy as np
import pandas as pd

from .agents import Agent, ABSTAIN
from .simulate import generate_regime_events


@dataclass
class EpisodeConfig:
    """Configuration parameters for an episode simulation.

    Attributes:
        risk_budget: Starting risk budget at the beginning of each episode.
        incorrect_penalty: Amount of risk budget consumed by an incorrect action.
        unsafe_penalty: Amount of risk budget consumed by an unsafe action.
    """

    risk_budget: float = 1.0
    incorrect_penalty: float = 0.5
    unsafe_penalty: float = 0.8


def run_episode(
    agent: Agent,
    regime: str,
    n_steps: int,
    seed: int,
    cfg: EpisodeConfig | None = None,
) -> Tuple[bool, int]:
    """Run a single episode for a given agent and regime.

    An episode is a sequence of ``n_steps`` synthetic events drawn from the
    specified regime.  The provided agent makes a decision for each event.
    The episode ends early if the risk budget is exhausted.

    Args:
        agent: Policy agent implementing a ``decide`` method.
        regime: Name of the regime (see ``simulate.REGIME_CONFIGS``).
        n_steps: Number of timesteps to simulate within the episode.
        seed: Random seed for event generation; each episode should use a
            different seed to avoid correlated sequences.
        cfg: Optional ``EpisodeConfig`` specifying risk budget and penalties.

    Returns:
        A tuple ``(failure, steps_taken)`` where ``failure`` is ``True`` if
        the episode ended because the risk budget was exhausted, and
        ``steps_taken`` is the number of timesteps processed until
        termination (``≤ n_steps``).
    """
    if cfg is None:
        cfg = EpisodeConfig()
    # Generate synthetic events for this episode with its own RNG
    events = generate_regime_events(regime=regime, n=n_steps, rng=np.random.default_rng(seed))
    risk = cfg.risk_budget
    steps = 0
    for _, row in events.iterrows():
        steps += 1
        decision = agent.decide(row)
        action = decision["action"]
        # Skip abstentions; no risk consumed
        if action == ABSTAIN:
            continue
        # Determine correctness and safety from the event
        prediction_correct = bool(row["predicted_direction"] == row["true_direction"])
        unsafe = bool(row["unsafe_condition"])
        # Apply penalties
        if not prediction_correct:
            risk -= cfg.incorrect_penalty
        if unsafe:
            risk -= cfg.unsafe_penalty
        if risk <= 0:
            return True, steps
    return False, steps


def evaluate_agent_episodes(
    agent: Agent,
    regime: str,
    n_episodes: int = 50,
    n_steps: int = 100,
    seed_offset: int = 1234,
    cfg: EpisodeConfig | None = None,
) -> Dict[str, float]:
    """Run multiple episodes and compute failure statistics for an agent/regime.

    Args:
        agent: Policy agent.
        regime: Regime to simulate.
        n_episodes: Number of episodes to run.
        n_steps: Maximum steps per episode.
        seed_offset: Seed offset so each episode uses a different seed.
        cfg: Episode configuration.

    Returns:
        A dictionary with the failure rate and the mean number of steps before
        failure (or episode completion).
    """
    failures = 0
    steps_before_end: list[int] = []
    for i in range(n_episodes):
        failure, steps = run_episode(agent, regime, n_steps, seed=seed_offset + i, cfg=cfg)
        if failure:
            failures += 1
        steps_before_end.append(steps)
    fail_rate = failures / n_episodes if n_episodes else float("nan")
    mean_steps = float(np.mean(steps_before_end)) if steps_before_end else float("nan")
    return {
        "failure_rate": fail_rate,
        "mean_steps": mean_steps,
    }