# Daily Quote Generator

Utility that provides a deterministic "Quote of the Day" from a curated list. No network required.

## Usage

```bash
python -m daily_quote_generator.src.quote   # prints today's quote
```

Or import `get_quote` from `src/quote.py`:

```python
from daily_quote_generator.src.quote import get_quote
print(get_quote())
```

## How it works

- Quotes are stored in `data/quotes.json`.
- Selection is based on a SHA‑256 hash of the ISO date string, modulo the number of quotes.
- You can pass an explicit `datetime.date` to `get_quote` for reproducible results.

## Testing

Run the test suite with:

```bash
pytest utils/daily-quote-generator/tests
```
