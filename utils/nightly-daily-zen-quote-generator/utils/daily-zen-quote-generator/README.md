# Daily Zen Quote Generator

A tiny utility that returns a deterministic "quote of the day" from a curated list. The quote changes each day based on the calendar date, but is reproducible offline—perfect for terminal greetings, CI logs, or Slack bots.

## Features

- No external network calls; all quotes are bundled.
- Deterministic: the same date always yields the same quote.
- Simple CLI: `python -m daily_zen_quote_generator` prints today’s quote.
- Library API: `get_quote(date)` returns the quote for any `datetime.date`.

## Installation

Copy the `utils/daily-zen-quote-generator` folder into your repo. No extra dependencies beyond the Python standard library.

## Usage

```bash
$ python -m daily_zen_quote_generator
🌿 “The only true wisdom is in knowing you know nothing.” – Socrates
```

Or as a library:

```python
from src.main import get_quote
import datetime

print(get_quote(datetime.date(2023, 10, 31)))
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/daily-zen-quote-generator/tests
```
