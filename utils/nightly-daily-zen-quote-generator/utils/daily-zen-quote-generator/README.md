# Daily Zen Quote Generator

A whimsical yet practical utility that provides a deterministic "Zen" quote for any given date. Perfect for sprinkling inspiration into scripts, CI pipelines, or your terminal MOTD.

## Features

- No external dependencies or network calls.
- Deterministic output: the same date always yields the same quote.
- Simple CLI (`python -m daily_zen_quote_generator`) prints today's quote.
- Easy to import as a library.

## Installation

```bash
pip install .
# or copy the utils/daily-zen-quote-generator folder into your project
```

## Usage

```python
from src.quote import get_quote
print(get_quote())  # today's quote
# Or specify a date:
import datetime
print(get_quote(datetime.date(2023, 1, 1)))  # => "Stay hungry."
```

## Adding Your Own Quotes

Edit `src/quote.py` and modify the `QUOTES` list.

## License

MIT
