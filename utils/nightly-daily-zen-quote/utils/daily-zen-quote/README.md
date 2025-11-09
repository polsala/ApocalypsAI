# Daily Zen Quote

A tiny, self‑contained Python utility that returns a *daily* Zen‑style quote. The quote is deterministic – it is derived from the current calendar date, so the same date always yields the same quote without any network calls.

## Features

- **Zero external dependencies** – pure Python standard library.
- **Deterministic** – the quote for a given date never changes.
- **CLI friendly** – `python -m daily_zen_quote` prints today’s quote.
- **Tested** – includes offline unit tests that mock the date.

## Usage

```bash
# As a module
python -m daily_zen_quote

# Or import in your code
from daily_zen_quote.src.quote import get_daily_quote
print(get_daily_quote())
```

## How it works

The utility stores a static list of ~30 Zen quotes. It computes the day‑of‑year (1‑366) for the supplied date (or today) and selects a quote by taking the modulo of the list length. This yields a repeatable, evenly‑distributed rotation of quotes throughout the year.
