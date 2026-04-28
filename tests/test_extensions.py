import pandas as pd

from src.failure_replay import replay_failures
from src.run_multi_seed import run_multi_seed
from src.sweep import run_sweep
from src.static_vs_dynamic import compare_static_dynamic
from src.run_episodes import run as run_episodes


def test_run_multi_seed_returns_expected_columns():
    df = run_multi_seed(seeds=[1, 2], n_per_regime=5)
    assert not df.empty
    assert "toy_safety_score_mean" in df.columns
    assert "unsafe_action_rate_mean" in df.columns


def test_threshold_sweep_smoke():
    df = run_sweep(
        confidence_thresholds=[0.60],
        volatility_limits=[0.70],
        monitor_limits=[0.55],
        n_per_regime=5,
        seed=1,
    )
    assert not df.empty
    assert {"coverage_mean", "unsafe_action_rate_mean"}.issubset(df.columns)


def test_failure_replay_empty_result_does_not_crash():
    df = replay_failures(
        agent_name="ConservativeAbstentionAgent",
        regime="liquidity_crash",
        n=5,
        n_events=10,
        seed=42,
    )
    assert "risk_score" in df.columns


def test_static_vs_dynamic_smoke():
    df = compare_static_dynamic(n_per_regime=5, seed=1)
    assert not df.empty
    assert "unsafe_rate_increase" in df.columns


def test_run_episodes_writes_summary(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    run_episodes(n_episodes=2, n_steps=5, seed_offset=10)
    out = tmp_path / "results" / "episode_summary.csv"
    assert out.exists()
    df = pd.read_csv(out)
    assert not df.empty
