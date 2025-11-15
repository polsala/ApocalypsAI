# Daily Zen Quote Generator

A tiny, whimsical utility that prints a *quote of the day*.

## Features

- Deterministic selection based on the current date (no randomness, no network).
- Built‑in collection of 30 Zen‑style quotes.
- Simple CLI: `python -m daily_zen_quote` or `daily-zen-quote` after installing.
- Zero external dependencies – pure Python 3.11.

## Usage

```bash
$ python -m daily_zen_quote
# or after installing as a script
$ daily-zen-quote
```

## Implementation

The utility lives in `src/main.py`. It calculates the day‑of‑year, mods it by the number of quotes, and prints the selected quote.

## Tests

Run the test suite with:

```bash
python -m unittest discover -s utils/daily-zen-quote-generator/tests
```
