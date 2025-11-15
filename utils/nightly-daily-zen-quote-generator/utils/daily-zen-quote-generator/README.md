# Daily Zen Quote Generator

A tiny, self‑contained Python utility that returns a *deterministic* Zen‑style quote for the current day. The quote changes once per day and is derived from a static list, so it works offline and is fully reproducible.

## Features
- No external network calls – all quotes are bundled.
- Deterministic: the same date always yields the same quote.
- Simple CLI: `python -m daily_zen_quote` prints today’s quote.
- Easy to embed in scripts, CI pipelines, or terminal prompts.

## Usage
```bash
# Run the module directly
python -m daily_zen_quote

# Or import in your own code
from daily_zen_quote import get_today_quote
print(get_today_quote())
```

## Implementation Details
- Quotes are stored in `src/quotes.json`.
- The index is computed as `hash(date) % len(quotes)` using Python's built‑in `hash` on the ISO date string, ensuring the same result across runs.
- The CLI uses `argparse` for future extensibility.

## Testing
Run the tests with:
```bash
python -m unittest discover -s utils/daily-zen-quote-generator/tests
```
The tests mock the current date to guarantee deterministic output.
