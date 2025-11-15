# Daily Zen Quote Generator

A tiny, self‑contained utility that prints a *quote of the day*.

## What it does
- Holds a small list of timeless Zen‑style quotes.
- Selects a quote deterministically from the current UTC date (no external APIs).
- Provides a simple CLI (`python -m src.main`) that prints the quote.

## Usage
```bash
# From the utility folder
python -m src.main
```
Will output something like:
```
Simplicity is the ultimate sophistication.
```

## How it works
The quote is chosen by taking the ordinal value of the date (`date.toordinal()`) and applying modulo the number of quotes. This guarantees the same date always yields the same quote, while different dates cycle through the list.

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s tests
```
All tests are deterministic and run offline.
