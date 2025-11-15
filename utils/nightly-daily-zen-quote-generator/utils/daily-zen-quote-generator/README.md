# Daily Zen Quote Generator

A tiny Python utility that prints a daily Zen quote. The quote is deterministic based on the current date, requiring no network access.

## Features

- No external dependencies.
- Deterministic output (same date → same quote).
- Simple CLI: `python -m zen_quote` prints today's quote.
- Easy to embed in scripts or terminal prompts.

## Usage

```bash
python -m zen_quote
# or
python utils/daily-zen-quote-generator/src/zen_quote.py
```

## Adding Quotes

Edit the `QUOTES` list in `zen_quote.py` to customize.

## Testing

Run:

```bash
python -m unittest discover utils/daily-zen-quote-generator/tests
```
