# Daily Zen Quote Generator

A whimsical yet useful command‑line tool that prints a random Zen‑style quote each time you run it. You can also request a quote from a specific theme (e.g., *mindfulness*, *impermanence*).

## Features
- Zero external dependencies – all quotes are baked into the package.
- Deterministic unit tests using `unittest.mock` to control randomness.
- Simple CLI: `python -m daily_zen_quote_generator [--tag TAG]`

## Installation
```bash
# From the repository root
cd utils/daily-zen-quote-generator
python -m venv .venv
source .venv/bin/activate
pip install .
```

## Usage
```bash
# Random quote
python -m daily_zen_quote_generator

# Quote from a specific tag
python -m daily_zen_quote_generator --tag mindfulness
```

## Development & Testing
```bash
# Run the test suite
pytest -q
```
