# Daily Zen Quote Generator

A lightweight, offline utility that prints a random Zen‑style quote each time you run it.

## Features
- **Zero external dependencies** – pure Python 3.11.
- Bundles a curated list of ~20 Zen quotes in `quotes.json`.
- Optional `--author` flag to limit results to a specific author.
- Deterministic unit tests using mocks (no network, no randomness).

## Usage
```bash
python -m daily_zen_quote_generator
# or with author filter
python -m daily_zen_quote_generator --author "Shunryu Suzuki"
```

## Files
- `src/main.py` – implementation and CLI entry point.
- `src/quotes.json` – static quote database.
- `tests/test_main.py` – deterministic tests with mocked I/O and randomness.
