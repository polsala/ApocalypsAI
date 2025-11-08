# Daily Zen Quote Generator

A lightweight, offline utility that prints a *zen* quote for the day. The quote is chosen deterministically based on the calendar date, so the same date always yields the same quote.

## Features
- No external network access – all quotes are bundled.
- Deterministic selection (useful for reproducible builds or tests).
- Simple CLI: `python -m daily_zen_quote_generator`.
- Easy to embed in scripts, CI pipelines, or daily terminal greetings.

## Usage
```bash
# Run the generator (prints today's quote)
python -m daily_zen_quote_generator

# Or import the function in your own code
from daily_zen_quote_generator import get_quote
print(get_quote())
```

## How it works
1. A small JSON file (`quotes.json`) stores an array of zen‑style sayings.
2. The utility computes `index = (date.toordinal()) % len(quotes)`.
3. The quote at that index is returned.

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/daily-zen-quote-generator/tests
```
All tests are deterministic and use mocks; no internet required.
