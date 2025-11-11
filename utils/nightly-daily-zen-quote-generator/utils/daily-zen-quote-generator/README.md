# Daily Zen Quote Generator

A lightweight, offline utility that prints a *Zen* quote for the current day.

## Features
- No external dependencies – pure Python 3.11.
- Deterministic: the same date always yields the same quote.
- Simple CLI: `python -m daily_zen_quote_generator`.
- Fully tested with mocked dates.

## Usage
```bash
$ python -m daily_zen_quote_generator
🧘  "The journey of a thousand miles begins with one step."
```

## How it works
The utility ships with a small JSON‑style list of quotes. The current date (year, month, day) is converted to an integer seed, which selects a quote via modulo arithmetic. This guarantees that each day maps to a single, repeatable quote without any network calls.

## Development
Run the test suite with:
```bash
python -m unittest discover -s utils/daily-zen-quote-generator/tests
```
