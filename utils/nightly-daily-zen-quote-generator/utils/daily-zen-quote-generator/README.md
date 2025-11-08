# Daily Zen Quote Generator

A whimsical yet practical command‑line tool that prints a Zen‑style quote for a given date.

## Features
- Deterministic: the same date always yields the same quote.
- No external network calls – all quotes are bundled.
- Simple CLI: `python -m daily_zen_quote <YYYY-MM-DD>`
- Easy to embed in CI pipelines, commit hooks, or daily stand‑up notes.

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
python -m daily_zen_quote 2025-11-08
# → "The river flows, but the stone remains."
```

## Testing
```bash
pytest -q
```
