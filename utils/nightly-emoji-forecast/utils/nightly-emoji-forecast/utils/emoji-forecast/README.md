# Emoji Forecast Utility

**Purpose**: Provide a fun, deterministic weather forecast expressed entirely in emojis for any given date. Perfect for adding a splash of personality to chat messages, daily stand‑ups, or commit logs.

## Features
- Deterministic output: the same date always yields the same emoji pair.
- No external dependencies – pure Python 3.11 standard library.
- Simple CLI (`python -m src.forecast`) and importable function.

## Usage
```bash
# Get today's forecast
python -m src.forecast

# Get forecast for a specific date
python -m src.forecast --date 2025-12-25
```

Or as a library:
```python
from src.forecast import get_forecast
print(get_forecast(date=datetime.date(2025, 12, 25)))
```

## How it works
The utility hashes the ISO‑formatted date with SHA‑256, converts the hash to an integer, and maps that integer to two emojis from a fixed list. Because the hash is deterministic, the same date always produces the same emoji pair.

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s tests
```
