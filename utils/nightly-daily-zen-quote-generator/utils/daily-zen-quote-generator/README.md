# Daily Zen Quote Generator

A self‑contained utility that prints a deterministic *quote of the day*.

## What it does
- Holds a small curated list of Zen‑style quotes.
- Picks a quote based on the current UTC date (or a user‑provided date) using a simple deterministic formula.
- No external network access – everything lives inside the utility.

## Usage
```bash
# Install (just copy the folder into your repo and run the script)
python -m utils.daily-zen-quote-generator.src.main

# Or get a quote for a specific date
python -m utils.daily-zen-quote-generator.src.main 2023-12-31
```

## How it works
The quote index is calculated as:
```
(year + month + day) % len(quotes)
```
Because the calculation is pure arithmetic, the same date always yields the same quote, making the utility fully deterministic and testable offline.

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/daily-zen-quote-generator/tests
```
