# Daily Zen Quote

`daily-zen-quote` is a lightweight, zero‑dependency Python utility that prints a *deterministic* Zen‑style quote for the current day (or any supplied date). The quote is chosen from a small built‑in collection, making the tool completely offline and reproducible.

## Features
- No external network calls – all quotes are bundled.
- Deterministic selection based on the calendar date, so the same date always yields the same quote.
- Simple CLI: `python -m daily_zen_quote` prints today’s quote.
- Easy to embed in scripts, CI pipelines, or terminal prompts.

## Installation
```bash
# From the repository root
cd utils/daily-zen-quote
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage
```bash
# Print today's quote
python -m daily_zen_quote

# Print a quote for a specific date (YYYY-MM-DD)
python -m daily_zen_quote 2023-01-01
```

## Development & Testing
```bash
# Run the test suite
pytest
```

## License
MIT © ApocalypsAI
