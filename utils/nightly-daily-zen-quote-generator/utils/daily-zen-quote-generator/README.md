# Daily Zen Quote Generator

A tiny, self‑contained Python utility that prints a random Zen‑style quote.  It can be seeded for deterministic output, making it perfect for:

* Adding a calming line to CI logs or terminal prompts.
* Generating a daily quote in scripts or cron jobs.
* Demonstrating deterministic randomness in teaching material.

## Features

* **Zero external dependencies** – only the Python standard library.
* **Deterministic mode** – supply `--seed <int>` to get the same quote every run.
* **Simple CLI** – `python -m src.quote_generator [--seed N]`.
* **Fully tested** – includes offline, deterministic unit tests.

## Installation

```bash
# Clone the repository (or copy the folder) and install the utility locally
cd utils/daily-zen-quote-generator
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

> The utility is deliberately lightweight; you can also just run the module directly without installing.

## Usage

```bash
# Random quote (non‑deterministic)
python -m src.quote_generator

# Deterministic quote – same output every time with the same seed
python -m src.quote_generator --seed 42
```

## Development & Testing

```bash
# Run the test suite
pytest -q
```

The tests are offline and use only the standard library.
