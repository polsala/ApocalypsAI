# Whimsical Quote of the Day

A tiny, self‑contained Python utility that returns a deterministic, day‑based quote from a curated list of whimsical sayings.

## Features
- **Deterministic**: The same calendar day always yields the same quote.
- **Zero external dependencies** – pure Python 3.11.
- **CLI & library**: Use it from the command line or import the `get_quote` function.
- **Fully tested** with offline, deterministic unit tests.

## Installation
```bash
# From the repository root
cd utils/whimsical-quote-of-the-day
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage
```bash
# As a script
python -m src.quote

# As a library
>>> from src.quote import get_quote
>>> get_quote()
"The early bird gets the worm, but the second mouse gets the cheese."
```

## How it works
The utility stores a short list of quotes. It computes the day‑of‑year (1‑365) for the current date and selects a quote using modulo arithmetic:
```python
index = (day_of_year - 1) % len(QUOTES)
```
Thus the mapping is repeatable and requires no network access.

## Testing
Run the test suite with:
```bash
pytest -q
```
All tests are deterministic and use mocks where appropriate.
