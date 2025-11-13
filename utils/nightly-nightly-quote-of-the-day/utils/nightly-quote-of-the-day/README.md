# Nightly Quote of the Day

A whimsical yet useful utility that prints a random motivational quote to the console.

## Features
- Built‑in collection of quotes with optional tags (e.g., *inspiration*, *humor*).
- Simple CLI: `python -m quote [--tag TAG]`.
- No external dependencies, works offline.
- Deterministic unit tests using mocks.

## Usage
```bash
# Print any random quote
python -m quote

# Print a random quote tagged with "inspiration"
python -m quote --tag inspiration
```

## Structure
- `src/quote.py` – core implementation.
- `tests/test_quote.py` – unit tests.
