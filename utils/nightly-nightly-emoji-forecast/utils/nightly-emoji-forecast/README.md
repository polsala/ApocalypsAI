# Nightly Emoji Forecast

A tiny, self‑contained utility that spits out a three‑emoji "weather" forecast for any date.

## Features
- **Deterministic** – the same date always yields the same forecast (uses an MD5 hash, no external randomness).
- **Zero dependencies** – pure Python 3.11 standard library.
- **CLI & library** – run `python -m forecast` to see today's forecast or import `get_forecast` in your own code.

## Usage
```bash
# Print today's forecast
python -m forecast

# Print forecast for a specific date (YYYY‑MM‑DD)
python -m forecast 2023-01-01
```

Or as a module:
```python
from datetime import date
from src.forecast import get_forecast

print(get_forecast(date.today()))
```

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/nightly-emoji-forecast/tests
```
