# Daily Zen Quote Generator

A tiny, self‑contained Python utility that returns a *daily* Zen‑style quote. The quote is deterministic – it depends only on the current calendar date – so the same day always yields the same quote, and no network access is required.

## Features
- Zero external dependencies (standard library only).
- Deterministic output – perfect for reproducible builds or CI logs.
- Simple CLI: `python -m daily_zen_quote_generator` prints today’s quote.
- Easy to embed in other scripts via `from daily_zen_quote_generator import get_quote`.

## Usage
```bash
# As a module
python -m daily_zen_quote_generator

# As a library
>>> from daily_zen_quote_generator import get_quote
>>> print(get_quote())
```

## How it works
The utility stores a short list of Zen quotes. It computes the day‑of‑year (1‑365/366) for the given date (defaults to `datetime.date.today()`) and selects a quote by taking the modulo of the day number with the number of quotes. This yields a repeatable, evenly‑distributed mapping.

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/daily-zen-quote-generator/tests
```
All tests are deterministic and use mocks; no network calls are made.
