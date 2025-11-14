# Daily Zen Quote Generator

A self‑contained utility that prints a *deterministic* quote of the day based solely on the current date. No external APIs, no dependencies beyond the Python standard library.

## Features
- **Deterministic**: The same date always yields the same quote.
- **Zero network**: Works offline; quotes are baked into the package.
- **Simple CLI**: `python -m daily_zen_quote_generator` prints the quote.
- **Tested**: Includes unit tests that mock dates to guarantee repeatable results.

## Usage
```bash
python -m daily_zen_quote_generator
```
Will output something like:
```
The journey of a thousand miles begins with one step.
```

## Implementation Details
- Quotes are stored in a hard‑coded list.
- The quote index is calculated as `date.toordinal() % len(quotes)`.
- The module provides a `get_quote_of_day(date: datetime.date | None = None) -> str` function for programmatic use.
