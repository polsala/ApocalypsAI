# Daily Zen Quote Generator

A lightweight, offline utility that prints a deterministic "Zen" quote for the current day (or any given date).

## Features

- **Zero network dependency** – all quotes are stored locally.
- **Deterministic** – the same date always yields the same quote.
- **CLI friendly** – `python -m daily_zen_quote_generator` prints today’s quote.
- **Library friendly** – import `get_quote` for programmatic use.

## Installation

Copy the entire `utils/daily-zen-quote-generator` folder into your project and add the `src` directory to your `PYTHONPATH` or install it as a package.

```bash
# Example usage as a script
python -m daily_zen_quote_generator
```

## API

```python
from daily_zen_quote_generator import get_quote

# Get today's quote
print(get_quote())

# Get quote for a specific date (datetime.date instance)
import datetime
print(get_quote(datetime.date(2023, 1, 1)))
```

## Testing

Run the bundled tests with `pytest`:

```bash
cd utils/daily-zen-quote-generator
pytest -q
```

## License

MIT – see the repository root LICENSE file.
