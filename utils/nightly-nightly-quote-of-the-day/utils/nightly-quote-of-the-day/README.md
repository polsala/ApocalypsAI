# Nightly Quote of the Day

A self‑contained utility that prints a deterministic quote for the current day.

## Features
- No external network access – all quotes are baked into the package.
- Deterministic selection based on the day of the year, so the same date always yields the same quote.
- Simple CLI: `python -m quote_of_the_day` or `python src/quote_of_the_day.py`.
- Includes a tiny test suite that mocks the date.

## Usage
```bash
$ python -m quote_of_the_day
# "The only limit to our realization of tomorrow is our doubts of today." – Franklin D. Roosevelt
```

## Implementation Details
- Quotes are stored in a list inside `quote_of_the_day.py`.
- The index is computed as `(day_of_year - 1) % len(quotes)`.
- Tests patch `datetime.date.today` to ensure deterministic output.
