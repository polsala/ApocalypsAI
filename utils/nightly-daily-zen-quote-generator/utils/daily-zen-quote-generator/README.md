# Daily Zen Quote Generator

A tiny, self‑contained utility that returns a deterministic "zen" quote for any given date.

## Features
- **No external dependencies** – just the Python standard library.
- **Deterministic** – the same date always yields the same quote.
- **Lightweight CLI** – run it from the terminal to get today’s quote.
- **Reusable API** – import `get_zen_quote` in your own scripts.

## Installation
Copy the `utils/daily-zen-quote-generator` folder into your project and add it to your `PYTHONPATH` or install it as a package if you wish.

## Usage
```bash
# Print today’s quote
python -m daily_zen_quote_generator

# Print a quote for a specific date (YYYY-MM-DD)
python -m daily_zen_quote_generator 2023-10-31
```

Or as a library:
```python
from daily_zen_quote_generator import get_zen_quote
from datetime import date

print(get_zen_quote(date.today()))
```

## How it works
A static list of five timeless zen sayings is cycled through based on the day‑of‑year:
```python
index = (date.timetuple().tm_yday - 1) % len(QUOTES)
```
Thus each day maps to a predictable quote, and the pattern repeats every five days.

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/daily-zen-quote-generator/tests
```
All tests are deterministic and offline.
