# Daily Zen Quote Generator

A lightweight, zero‑dependency utility that prints a "Zen" quote of the day.

## Features
- Deterministic output based on the current date (no network calls).
- Built‑in list of five inspirational quotes.
- Simple CLI: `python -m daily_zen_quote_generator`.
- Fully tested with offline, deterministic unit tests.

## Usage
```bash
$ python -m daily_zen_quote_generator
The journey of a thousand miles begins with one step.
```

## Implementation Details
- The quote is selected by taking the ordinal of today's date modulo the number of quotes.
- All data lives in `src/quotes.json`; no external resources are required.
- Tests mock the date to guarantee repeatable results.
