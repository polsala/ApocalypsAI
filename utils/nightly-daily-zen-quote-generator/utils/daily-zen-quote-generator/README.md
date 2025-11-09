# Daily Zen Quote Generator

A lightweight, offline utility that prints a random Zen‑style quote each time you run it.

## Features

- **Zero external dependencies** – pure Python 3.11.
- Bundled `quotes.json` with a curated list of short, thought‑provoking sayings.
- Optional `--category` flag to limit quotes to a specific theme (e.g., *mindfulness*, *humor*).
- Deterministic unit tests that mock file I/O and randomness.

## Usage

```bash
python -m utils.daily-zen-quote-generator.src.main          # any quote
python -m utils.daily-zen-quote-generator.src.main --category mindfulness
```

## Development

Run the test suite with:

```bash
python -m unittest discover -s utils/daily-zen-quote-generator/tests
```
