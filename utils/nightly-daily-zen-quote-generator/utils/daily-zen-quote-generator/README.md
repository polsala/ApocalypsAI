# Daily Zen Quote Generator

A whimsical yet practical utility that prints a *quote of the day*.

## What it does
- Stores a curated list of short, zen‑like quotes.
- Picks a quote based on the current date, so the output is **deterministic** and changes once per day.
- Provides a tiny CLI (`python -m daily_zen_quote_generator`) that can be invoked from scripts, CI pipelines, or directly in the terminal.

## Installation
The utility is self‑contained and requires only the Python 3.11 standard library.

```bash
# From the repository root
python -m pip install -e utils/daily-zen-quote-generator
```

## Usage
```bash
# Print today’s quote
python -m daily_zen_quote_generator
```

You can also import the core function in your own code:
```python
from daily_zen_quote_generator import get_quote
print(get_quote())
```

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/daily-zen-quote-generator/tests
```

The tests mock the current date to ensure deterministic behaviour.
