# Daily Zen Quote Generator

A whimsical yet useful utility that prints a *Zen* quote of the day.

## Features
- No external dependencies or network access.
- Deterministic: the same date always yields the same quote.
- Simple CLI: `python -m daily_zen_quote_generator` prints the quote.
- Fully tested with offline, deterministic mocks.

## Usage
```bash
cd utils/daily-zen-quote-generator
python -m src.main
```

## How it works
The utility contains a small list of Zen‑style quotes. The quote for a given day is selected by hashing the ISO‑format date (`YYYY‑MM‑DD`) and using the result to index the list.

## Testing
```bash
python -m unittest discover -s tests
```
