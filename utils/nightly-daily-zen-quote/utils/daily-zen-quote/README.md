# Daily Zen Quote

A tiny, self‑contained utility that returns a *quote of the day* from a curated list of Zen‑style sayings. The quote is deterministic – it depends only on the current date, so the same day always yields the same quote.

## Features

- **Deterministic**: No network calls; the quote is derived from the date.
- **CLI**: `python -m daily_zen_quote` prints the quote for today.
- **Library**: `daily_zen_quote.get_quote(date)` returns the quote for any `datetime.date`.
- **Zero external dependencies** – pure Python 3.11 standard library.

## Usage

```bash
# As a script (prints today's quote)
python -m daily_zen_quote

# As a library
>>> from daily_zen_quote import get_quote
>>> get_quote()
"The obstacle is the path."
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/daily-zen-quote/tests
```

The tests mock the current date to guarantee deterministic results.
