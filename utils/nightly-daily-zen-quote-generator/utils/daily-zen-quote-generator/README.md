# Daily Zen Quote Generator

A tiny, self‑contained Python utility that prints a deterministic "Zen" quote for today (or any supplied date). The quote is chosen from a short built‑in list using a reproducible algorithm based on the ISO week number, so the same date always yields the same quote.

## Features
- Zero external dependencies (only the Python standard library).
- Works as a CLI tool (`zen-quote`) and as an importable function.
- Deterministic output – great for CI logs, daily emails, or terminal prompts.
- Fully tested with offline, deterministic unit tests.

## Installation
```bash
# Clone the repository (or copy the folder) and install the utility in a venv
python -m venv .venv
source .venv/bin/activate
pip install -e utils/daily-zen-quote-generator
```

## Usage
```bash
# Print today's quote
zen-quote

# Print the quote for a specific date
zen-quote --date 2023-01-02
```

## API
```python
from utils.daily-zen-quote-generator.src.main import get_quote

# Get today's quote
print(get_quote())

# Get quote for a specific date
import datetime
print(get_quote(datetime.date(2023, 1, 2)))
```

## Testing
```bash
python -m unittest discover utils/daily-zen-quote-generator/tests
```
