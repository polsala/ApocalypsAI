# Daily Zen Quote Generator

Utility that prints a random Zen‑inspired quote, optionally filtered by a keyword. No external network calls; all quotes are bundled.

## Installation

```bash
# The utility is self‑contained; you can run it directly with Python 3.11.
python -m utils.daily-zen-quote-generator.src.quote_generator
```

## Usage

```bash
# Print a random quote
python -m utils.daily-zen-quote-generator.src.quote_generator

# Print a random quote containing a keyword (case‑insensitive)
python -m utils.daily-zen-quote-generator.src.quote_generator --keyword peace
```

## How it works

- Quotes are stored in `src/quote_generator.py`.
- `get_random_quote` selects a random quote, optionally matching a keyword.
- A small CLI entrypoint is provided.

## Testing

```bash
python -m unittest discover -s utils/daily-zen-quote-generator/tests
```
