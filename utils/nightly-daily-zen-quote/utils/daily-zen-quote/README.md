# Daily Zen Quote

`daily-zen-quote` is a tiny, self‑contained Python utility that returns a Zen‑style quote that changes each day. The quote is deterministic – it is derived from the current date, so the same date always yields the same quote. This makes it safe for offline use and perfect for embedding in logs, CI pipelines, or as a daily terminal greeting.

## Features

- **Zero external dependencies** – pure Python 3.11 standard library.
- **Deterministic** – the quote for a given date never changes.
- **CLI & library** – use it as a command‑line tool or import the function in your own code.
- **Fully tested** – includes offline unit tests with no network calls.

## Installation

Copy the `utils/daily-zen-quote` folder into your repository and run:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt  # (no extra requirements needed)
```

## Usage

### As a library

```python
from src.quote import get_daily_quote

# Get today's quote
print(get_daily_quote())

# Get quote for a specific date (useful for testing)
from datetime import date
print(get_daily_quote(date(2025, 1, 1)))
```

### As a CLI tool

```bash
python -m src.quote          # prints today's quote
python -m src.quote --date 2025-01-01  # prints quote for a given date
```

## How it works

The utility stores a short list of Zen quotes. It computes the day‑of‑year for the supplied (or current) date, then selects a quote using modulo arithmetic:

```python
index = day_of_year % len(QUOTES)
```

Because the algorithm is pure and deterministic, the same date always maps to the same quote.

## Testing

Run the tests with:

```bash
python -m unittest discover -s tests
```

The test suite checks that the function returns the expected quote for known dates and that the CLI prints the same output.
