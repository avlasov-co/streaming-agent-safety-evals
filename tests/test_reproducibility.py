from src.simulate import generate_dataset


def test_dataset_generation_is_reproducible_for_same_seed():
    first = generate_dataset(n_per_regime=20, seed=123)
    second = generate_dataset(n_per_regime=20, seed=123)
    assert first.equals(second)
