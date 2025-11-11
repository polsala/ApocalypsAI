# Whimsical Quote of the Day

A lightweight, offline utility that prints a fun, deterministic quote based on the current date.

## Features
- No external dependencies.
- Deterministic selection: the same date always yields the same quote.
- Simple CLI (`python -m quote_of_the_day`) and importable function.
- Fully tested with mocked dates.

## Usage
```bash
# Run the CLI
python -m utils.whimsical-quote-of-the-day.src.quote_of_the_day
```

Or as a library:
```python
from utils.whimsical-quote-of-the-day.src.quote_of_the_day import get_quote_of_the_day
print(get_quote_of_the_day())
```

## Adding New Quotes
Edit `src/quote_of_the_day.py` and append to the `QUOTES` list. The utility will automatically incorporate them.
