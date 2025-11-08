# Daily Zen Quote Generator

A tiny utility that prints a deterministic "quote of the day" from a curated list. No network calls; works offline. Ideal for adding a splash of inspiration to your terminal or scripts.

## Usage

```bash
python -m daily_zen_quote_generator
```

or

```bash
python utils/daily-zen-quote-generator/src/main.py
```

## How it works

The quote is selected based on the current date. The algorithm hashes the ISO date string and picks a quote modulo the list length, ensuring the same date always yields the same quote.

## Adding quotes

Edit `src/quote.py` and extend the `QUOTES` list.

## Tests

Run:

```bash
python -m unittest discover utils/daily-zen-quote-generator/tests
```
