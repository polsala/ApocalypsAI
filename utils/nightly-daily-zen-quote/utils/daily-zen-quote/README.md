# Daily Zen Quote

**Utility:** `daily-zen-quote`

A tiny, self‑contained Python utility that prints a deterministic "quote of the day" based on the current calendar date. It works completely offline – the list of quotes is baked into the code and the selection algorithm is deterministic, so the same date always yields the same quote.

## Features
- No external dependencies.
- Deterministic selection using `date.toordinal()`.
- Simple CLI (`python -m daily_zen_quote`) prints today’s quote.
- Programmatic API via `get_quote(date: datetime.date | None = None) -> str`.
- Fully tested with offline mocks.

## Installation & Usage
```bash
# From the repository root
python -m utils.daily-zen-quote.src.quote   # prints today’s quote
```
Or import in your own code:
```python
from utils.daily-zen-quote.src.quote import get_quote
print(get_quote())  # today’s quote
print(get_quote(datetime.date(2022, 12, 25)))  # quote for a specific date
```

## How it works
The utility stores a short list of Zen‑style sayings. The index is computed as:
```python
index = date.toordinal() % len(_QUOTES)
```
Because `date.toordinal()` is a monotonically increasing integer, the same date always maps to the same index.

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/daily-zen-quote/tests
```
All tests are deterministic and use `unittest.mock` to avoid any real date or network calls.
