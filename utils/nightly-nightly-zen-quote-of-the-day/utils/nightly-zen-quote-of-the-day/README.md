# Nightly Zen Quote of the Day

A tiny utility that prints a random Zen‑inspired quote to the console. Perfect for adding a moment of reflection to your terminal or CI runs.

## Usage

```bash
python utils/nightly-zen-quote-of-the-day/src/quote.py
```

You can also import the helper functions in your own scripts:

```python
from src.quote import get_random_quote, load_quotes
```

## How it works

- Quotes are stored in `data/quotes.json`.
- `quote.py` loads the JSON file and selects a random entry.
- The selection is deterministic in tests via mocking.

## Testing

```bash
python -m unittest discover utils/nightly-zen-quote-of-the-day/tests
```
