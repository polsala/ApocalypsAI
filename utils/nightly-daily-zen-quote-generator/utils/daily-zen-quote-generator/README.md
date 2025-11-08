# Daily Zen Quote Generator

A whimsical yet practical command‑line tool that provides a deterministic Zen‑style quote for a given date.

## Features
- **Deterministic**: The same date always yields the same quote.
- **Offline**: No network calls; quotes are baked into the utility.
- **Lightweight**: Pure Python 3.11, no external dependencies.
- **CLI & Library**: Use it from the command line or import the `get_quote` function in your own scripts.

## Installation
```bash
# From the repository root
cd utils/daily-zen-quote-generator
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage
```bash
# Get today's quote
python -m daily_zen_quote_generator

# Get quote for a specific date (YYYY‑MM‑DD)
python -m daily_zen_quote_generator 2025-12-31
```

## Library API
```python
from daily_zen_quote_generator import get_quote
from datetime import date

quote = get_quote(date.today())
print(quote)
```

## Testing
```bash
pytest
```

## License
MIT © ApocalypsAI
