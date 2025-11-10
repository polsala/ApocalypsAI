# Daily Motivation Generator

A self‑contained Python utility that prints a daily motivational quote. The quote is **deterministic** – it depends only on the current date, so the same day always yields the same output. No network access, no external data files, and no third‑party dependencies.

## Features

- Offline – works anywhere Python 3.11+ is available.
- Deterministic selection based on the date (useful for reproducible tests).
- Optional ASCII‑art banner for extra whimsy.
- Simple CLI: `python -m daily_motivation_generator`

## Usage

```bash
$ python -m daily_motivation_generator
🌞 Good morning! "The only limit to our realization of tomorrow is our doubts of today." – Franklin D. Roosevelt
```

You can also import the core function:

```python
from daily_motivation_generator import get_quote_for_date
print(get_quote_for_date(date(2025, 12, 25)))
```

## Implementation Details

- Quotes are stored in a hard‑coded list inside the package.
- The index is computed as `hash(date.isoformat()) % len(QUOTES)` which guarantees the same result for the same date across runs and platforms.
- The optional banner is printed when the environment variable `MOTIVATION_BANNER` is set to any non‑empty value.

## Testing

Run the test suite with:

```bash
python -m unittest discover -s utils/daily-motivation-generator/tests
```
