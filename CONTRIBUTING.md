# Contributing

This repository is intentionally small and research-oriented. Contributions should preserve the main goal: evaluating agentic behavior under distribution shift, uncertainty, and unsafe overconfident conditions.

Useful contributions include:

- New deployment regimes with clear failure modes
- New safety metrics
- Additional baseline agents
- Better plots and reports
- Tests that improve reproducibility

Avoid adding:

- Real trading strategies
- Exchange integrations
- API keys or secrets
- Private datasets
- Proprietary model code or weights

## Local check

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python -m src.run_eval --n-per-regime 300 --seed 42 --bootstrap 40
python -m src.plot_results
python -m src.generate_report
python -m pytest -q
```
