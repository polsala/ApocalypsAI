# Daily Zen Quote Generator

Utility that prints a calming Zen‑inspired quote for the current day. No network calls; quotes are baked in. Deterministic: the same date always yields the same quote.

## Usage

```bash
# Run the script (prints today’s quote)
python -m daily_zen_quote_generator
# or directly
python src/main.py
```

You can also supply an explicit date (ISO format) for testing or curiosity:

```bash
python src/main.py 2023-03-15
```

## How it works

The quote is selected by computing `(day_of_year - 1) % len(quotes)`. This guarantees a repeatable mapping from any calendar date to one of the built‑in quotes.

## Tests

Run the test suite with:

```bash
python -m unittest discover -s tests
```
