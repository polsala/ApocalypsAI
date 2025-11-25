# Nightly Zen Quote of the Day

A tiny utility that prints a random Zen‑inspired quote from a curated list. Perfect for adding a moment of reflection to your terminal or CI logs.

## Usage

```bash
python -m src.zen_quote
```

or

```bash
python utils/nightly-zen-quote-of-the-day/src/zen_quote.py
```

## How it works

- Maintains an internal list of ~10 quotes.
- Uses `random.choice` to select one.
- Provides `get_quote()` for programmatic use.

## Testing

Run:

```bash
pytest -q utils/nightly-zen-quote-of-the-day/tests
```
