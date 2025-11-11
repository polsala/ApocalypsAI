# Daily Zen Quote Generator

A whimsical yet practical utility that prints a *deterministic* Zen‑style quote for the current day (or any supplied date). No network calls – all quotes are bundled locally.

## Features
- Offline – works without internet.
- Deterministic – the same date always yields the same quote.
- Tiny – < 100 KB, pure Python 3.11, no external dependencies.
- CLI & library usage.

## Installation
```bash
# From the repository root
cd utils/daily-zen-quote-generator
python -m venv .venv
source .venv/bin/activate
pip install .
```

## Usage
### CLI
```bash
python -m daily_zen_quote_generator
# or, after installing as a package
daily-zen-quote
```
Outputs something like:
```
"The journey of a thousand miles begins with one step." – Lao Tzu
```

### Library
```python
from daily_zen_quote_generator import get_quote

quote = get_quote()  # uses today
print(quote)
```

## Testing
```bash
pytest
```
All tests are deterministic and run offline.
