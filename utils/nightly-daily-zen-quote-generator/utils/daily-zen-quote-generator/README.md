# Daily Zen Quote Generator

A whimsical yet practical command‑line tool that provides a deterministic Zen‑style quote for any date.

## Features
- **Offline** – No network calls; quotes are baked into the package.
- **Deterministic** – The same date always yields the same quote, making tests reliable.
- **Lightweight** – Pure Python 3.11, no external dependencies.

## Installation
```bash
# From the repository root
cd utils/daily-zen-quote-generator
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage
```bash
python -m daily_zen_quote_generator 2025-11-08
# → "The river flows, but the stones remain."
```

If no date is supplied, it defaults to today’s date.

## Development
Run the test suite with:
```bash
pytest -q
```

## License
MIT – see the root LICENSE file.
