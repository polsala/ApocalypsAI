# Nightly Quote of the Day

Utility that prints a random inspirational quote from a small built‑in collection. No network access is required; everything runs locally.

## Features
- Random quote on each run.
- Optional `--category` flag to filter quotes (e.g., `inspiration`, `life`, `wisdom`, `humor`, `fiction`).
- Fully self‑contained – just Python 3.11 standard library.

## Usage
```bash
python -m src.quote            # any random quote
python -m src.quote --category inspiration   # only inspirational quotes
```

## Adding New Quotes
Edit the `_QUOTES` list in `src/quote.py`. Each entry is a tuple of `(text, author, category)`.

## Testing
Run the test suite with:
```bash
python -m unittest discover -s tests
```
All tests are deterministic and use mocks where randomness is involved.
