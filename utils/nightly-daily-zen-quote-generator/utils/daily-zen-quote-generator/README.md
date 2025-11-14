# Daily Zen Quote Generator

A whimsical yet useful utility that provides a deterministic "Zen" quote for any given day. The quote is selected from a curated list and is reproducible across runs, making it ideal for:

- Adding a calming line to CI/CD logs.
- Displaying a daily mantra in terminal prompts.
- Embedding in scripts that need a touch of inspiration without external network calls.

## Features

- **Zero external dependencies** – pure Python 3.11 standard library.
- **Deterministic** – the same date always yields the same quote.
- **Offline** – no network requests; all quotes are bundled.
- **Simple CLI** – `python -m daily_zen_quote_generator` prints today’s quote.

## Installation

Copy the `utils/daily-zen-quote-generator` folder into your project and add the `src` directory to your `PYTHONPATH` or install as a package:

```bash
pip install -e utils/daily-zen-quote-generator
```

## Usage

```python
from daily_zen_quote_generator import get_daily_zen_quote

# Get today's quote
print(get_daily_zen_quote())

# Get quote for a specific date (datetime.date object)
import datetime
print(get_daily_zen_quote(datetime.date(2025, 1, 1)))
```

Or via the command line:

```bash
python -m daily_zen_quote_generator
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/daily-zen-quote-generator/tests
```

## License

MIT – see the repository LICENSE file.
