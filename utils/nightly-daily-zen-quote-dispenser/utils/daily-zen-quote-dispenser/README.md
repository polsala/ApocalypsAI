# Daily Zen Quote Dispenser

A **stand‑alone** Python utility that returns a random Zen‑style quote.

## Features

- Zero external dependencies (only the Python standard library).
- Provides a programmatic API (`get_zen_quote`) and a convenient CLI (`python -m daily_zen_quote_dispenser`).
- Fully tested with deterministic, offline unit tests.

## Installation

```bash
# Clone the repository (or copy the folder) and install in editable mode
pip install -e utils/daily-zen-quote-dispenser
```

## Usage

### As a library

```python
from daily_zen_quote_dispenser import get_zen_quote

print(get_zen_quote())
```

### From the command line

```bash
python -m daily_zen_quote_dispenser
# or
python utils/daily-zen-quote-dispenser/src/quote.py
```

## Testing

```bash
pytest utils/daily-zen-quote-dispenser/tests
```
