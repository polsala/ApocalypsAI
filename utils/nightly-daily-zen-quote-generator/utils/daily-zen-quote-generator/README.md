# Daily Zen Quote Generator

A tiny, self‑contained utility that prints a *Zen* quote of the day.

## Features

- **Deterministic**: The same date always yields the same quote.
- **Offline**: All quotes are bundled; no network calls.
- **CLI**: `python -m daily_zen_quote` prints the quote for today.
- **Library**: `get_quote_of_day(date: datetime.date | None = None) -> str` can be imported.

## Usage

```bash
# As a script
python -m daily_zen_quote

# As a library
from daily_zen_quote import get_quote_of_day
print(get_quote_of_day())
```

## Testing

Run the test suite with:

```bash
python -m unittest discover -s utils/daily-zen-quote-generator/tests
```

## Implementation Details

- Quotes are stored in `src/quotes.json`.
- The selection algorithm hashes the ISO‑format date string and takes the modulo of the quote count.
- The module is pure Python 3.11 with no external dependencies.
