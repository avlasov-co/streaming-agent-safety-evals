PYTHON ?= .venv/bin/python
SYSTEM_PYTHON ?= python3

.PHONY: setup install run run-fast plots report test multi-seed sweep episodes static-dynamic failure-replay aux-config smoke clean all

setup:
	$(SYSTEM_PYTHON) -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

install:
	$(PYTHON) -m pip install -r requirements.txt

run:
	$(PYTHON) -m src.run_eval --n-per-regime 3000 --seed 42 --bootstrap 250

run-fast:
	$(PYTHON) -m src.run_eval --n-per-regime 300 --seed 42 --bootstrap 40

plots:
	$(PYTHON) -m src.plot_results

report:
	$(PYTHON) -m src.generate_report

multi-seed:
	$(PYTHON) -m src.run_multi_seed --seeds 1 2 3 4 5 --n-per-regime 300

sweep:
	$(PYTHON) -m src.sweep --n-per-regime 100

episodes:
	$(PYTHON) -m src.run_episodes --n-episodes 10 --n-steps 30

static-dynamic:
	$(PYTHON) -m src.static_vs_dynamic --n-per-regime 300

failure-replay:
	$(PYTHON) -m src.failure_replay --agent NaiveAgent --regime adversarial_shift --n-events 300 --n 5

aux-config:
	$(PYTHON) -m src.write_aux_config

smoke: run-fast plots report multi-seed sweep episodes static-dynamic failure-replay aux-config

test:
	$(PYTHON) -m pytest -q

clean:
	rm -f results/*.csv results/*.json figures/*.png docs/experimental_report.md
	rm -rf .pytest_cache __pycache__ src/__pycache__ tests/__pycache__
	find . -name "*.pyc" -delete

all: run plots report multi-seed sweep episodes static-dynamic failure-replay aux-config test
