# Daily Zen Quote

`daily-zen-quote` is a lightweight, zero‑dependency Python utility that returns a **deterministic** "Zen" quote for the current day. The quote changes once per day and is derived solely from the date, making it completely offline and reproducible.

## Features
- No external network calls – works in air‑gapped environments.
- Deterministic mapping: the same date always yields the same quote.
- Simple CLI (`python -m src.quote`) prints today’s quote.
- Library function `get_zen_quote()` for programmatic use.

## Installation
```bash
# From the repository root
cd utils/daily-zen-quote
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage
### CLI
```bash
python -m src.quote
```
Outputs something like:
```
Be yourself; everyone else is already taken.
```

### As a library
```python
from src.quote import get_zen_quote
print(get_zen_quote())
```

## Testing
```bash
python -m unittest discover -s tests
```
All tests run offline and use mocks to guarantee deterministic results.
