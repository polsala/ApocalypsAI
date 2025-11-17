# Daily Motivation Quote Fetcher

A whimsical yet useful utility that prints a random motivational quote each time you run it.

## Features
- Built‑in collection of quotes (no network required).
- Optional `--theme` argument to filter quotes by theme (e.g., *perseverance*, *creativity*).
- Simple CLI: `python -m quote_fetcher [--theme THEME]`.
- Fully self‑contained with deterministic tests.

## Usage
```bash
# Print any random quote
python -m quote_fetcher

# Print a quote about perseverance
python -m quote_fetcher --theme perseverance
```

## Development
Run the test suite with:
```bash
python -m unittest discover -s utils/daily-motivation-quote-fetcher/tests
```
