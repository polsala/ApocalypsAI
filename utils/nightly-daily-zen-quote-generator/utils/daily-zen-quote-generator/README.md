# Daily Zen Quote Generator

A whimsical yet useful utility that prints a random Zen‑inspired quote to the console.  You can optionally filter quotes by a theme (e.g., `motivation`, `mindfulness`).

## Features
- Built‑in collection of short, uplifting quotes.
- Deterministic unit tests using mocks (offline, no network).
- Simple CLI (`python -m src.quote_generator [--theme THEME]`).

## Installation & Usage
```bash
# From the repository root
python -m utils.daily-zen-quote-generator.src.quote_generator
# With a theme filter
python -m utils.daily-zen-quote-generator.src.quote_generator --theme mindfulness
```

## Development
Run the test suite with:
```bash
python -m unittest discover -s utils/daily-zen-quote-generator/tests
```
