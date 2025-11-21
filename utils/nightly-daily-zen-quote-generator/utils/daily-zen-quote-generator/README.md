# Daily Zen Quote Generator

A whimsical yet useful utility that prints a random Zen‑style quote to stdout.

## Features
- No external dependencies – all quotes are bundled.
- Deterministic unit tests using a mock for `random.choice`.
- Simple CLI: `python -m daily_zen_quote_generator` prints a quote.

## Usage
```bash
python -m daily_zen_quote_generator
```

## Adding New Quotes
Edit the `QUOTES` list in `src/main.py` and re‑run the utility.
