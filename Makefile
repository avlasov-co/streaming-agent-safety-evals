.PHONY: setup run plots report test clean all

setup:
	python3 -m venv .venv
	. .venv/bin/activate && pip install -r requirements.txt

run:
	python3 -m src.run_eval --n-per-regime 3000 --seed 42

plots:
	python3 -m src.plot_results

report:
	python3 -m src.generate_report

test:
	python3 -m pytest -q

clean:
	rm -f results/*.csv results/*.json figures/*.png docs/experimental_report.md

all: run plots report test
