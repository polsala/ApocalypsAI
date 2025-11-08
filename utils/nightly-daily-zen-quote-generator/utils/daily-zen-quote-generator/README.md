# Daily Zen Quote Generator

A tiny, self‑contained utility that returns a Zen‑style quote for a given date.

## Features

- **Deterministic**: The same date always yields the same quote.
- **Zero external dependencies** – pure Python 3.11 standard library.
- **CLI**: `python -m daily_zen_quote_generator <YYYY-MM-DD>` prints the quote.
- **Library**: Import `get_zen_quote(date: datetime.date) -> str` in your own code.

## Usage

```bash
# As a script
python -m daily_zen_quote_generator 2025-11-08

# As a library
>>> from daily_zen_quote_generator import get_zen_quote
>>> get_zen_quote(date.today())
"The river never forgets its source."
```

## Implementation Details

The utility stores a short list of Zen quotes. It hashes the ISO‑format date, maps the hash to an index in the list, and returns the corresponding quote. This guarantees reproducibility without any randomness or network calls.

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/daily-zen-quote-generator/tests
```
