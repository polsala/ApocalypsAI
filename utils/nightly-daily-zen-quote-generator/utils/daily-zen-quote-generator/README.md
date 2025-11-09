# Daily Zen Quote Generator

A tiny, self‑contained utility that returns a *Zen* quote of the day.

## Features

- **Deterministic**: The same date always yields the same quote.
- **Zero external dependencies** – pure Python 3.11 standard library.
- **CLI & library usage** – import `get_daily_zen_quote` or run the script.

## Usage

```bash
# As a CLI tool
python -m daily_zen_quote_generator

# As a library
from daily_zen_quote_generator import get_daily_zen_quote
print(get_daily_zen_quote())
```

## How it works

A static list of 10 classic Zen sayings is stored in `quote.py`. The quote for a given day is selected by:

```python
index = (date.timetuple().tm_yday - 1) % len(QUOTES)
```

Thus the mapping repeats annually.

## Testing

Run the tests with:

```bash
python -m unittest discover -s utils/daily-zen-quote-generator/tests
```
