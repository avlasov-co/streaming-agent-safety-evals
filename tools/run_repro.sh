#!/usr/bin/env bash
set -euo pipefail

PYTHON_BIN="${PYTHON:-.venv/bin/python}"
CORE_N_PER_REGIME="${N_PER_REGIME:-3000}"
CORE_SEED="${SEED:-42}"
CORE_BOOTSTRAP="${BOOTSTRAP:-250}"
SMOKE_N_PER_REGIME="${SMOKE_N_PER_REGIME:-300}"

"$PYTHON_BIN" -m src.run_eval --n-per-regime "$CORE_N_PER_REGIME" --seed "$CORE_SEED" --bootstrap "$CORE_BOOTSTRAP"
"$PYTHON_BIN" -m src.plot_results
"$PYTHON_BIN" -m src.generate_report

# Reproduce the auxiliary shipped artifacts with lighter defaults.
"$PYTHON_BIN" -m src.run_multi_seed --seeds 1 2 3 4 5 --n-per-regime "$SMOKE_N_PER_REGIME"
"$PYTHON_BIN" -m src.sweep --n-per-regime "${SWEEP_N_PER_REGIME:-100}"
"$PYTHON_BIN" -m src.run_episodes --n-episodes 10 --n-steps 30
"$PYTHON_BIN" -m src.static_vs_dynamic --n-per-regime "$SMOKE_N_PER_REGIME"
"$PYTHON_BIN" -m src.failure_replay --agent NaiveAgent --regime adversarial_shift --n-events "$SMOKE_N_PER_REGIME" --n 5
"$PYTHON_BIN" -m src.write_aux_config

"$PYTHON_BIN" -m pytest -q
