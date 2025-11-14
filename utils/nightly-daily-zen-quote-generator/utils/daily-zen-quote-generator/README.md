# Daily Zen Quote Generator

Utility that prints a deterministic "Quote of the Day" selected from a curated list. The quote changes each day based on the calendar date, requiring no network access.

## Installation

```bash
pip install .
# or just run the script directly
```

## Usage

```bash
python -m daily_zen_quote_generator
# or
python utils/daily-zen-quote-generator/src/main.py
```

Outputs a single line quote.

## How it works

The script contains an internal list of quotes. The quote for a given day is chosen by computing `date.toordinal() % len(quotes)`. This ensures the same date always yields the same quote without external APIs.

## Testing

Run tests with:

```bash
python -m unittest discover utils/daily-zen-quote-generator/tests
```
