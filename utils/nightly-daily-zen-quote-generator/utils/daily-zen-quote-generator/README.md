# Daily Zen Quote Generator

A lightweight, self‑contained utility that prints a random Zen‑inspired quote.

## Features
- Returns a random quote from a built‑in collection.
- Optional `--tag` flag to filter quotes by thematic tags (e.g., `mindfulness`).
- Zero external dependencies – pure Python 3.11 standard library.
- Fully tested with deterministic, offline unit tests.

## Installation & Usage
```bash
# Clone the repository (or navigate to the utils folder)
cd utils/daily-zen-quote-generator

# Run the tool
python -m src.main            # prints a random quote
python -m src.main --tag zen   # prints a random quote tagged with "zen"
```

## Development
Run the test suite with:
```bash
python -m unittest discover -s tests
```

Feel free to add more quotes or tags in `src/main.py`.
