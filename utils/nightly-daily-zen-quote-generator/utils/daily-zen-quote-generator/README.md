# Daily Zen Quote Generator

Utility that returns a deterministic "quote of the day" from a curated list of Zen sayings. No network calls; works completely offline.

## Features
- Deterministic selection based on the current date.
- Small, self‑contained list of inspirational quotes.
- Usable as a CLI tool or as an importable Python function.

## Installation
```bash
# From the utility folder
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (no external deps required)
```

## Usage
### CLI
```bash
python -m src.main            # prints today's quote
python -m src.main --date 2023-01-01  # override date for testing
```

### As a library
```python
from src.main import get_quote_of_the_day
quote, author = get_quote_of_the_day()
print(f"{quote} — {author}")
```

## Testing
```bash
python -m unittest discover -s tests
```
