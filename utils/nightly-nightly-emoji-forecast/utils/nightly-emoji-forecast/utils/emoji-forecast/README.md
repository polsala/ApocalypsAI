# Emoji Forecast

Generate a whimsical daily emoji weather forecast.

## Usage

```bash
python -m src.forecast
# => 🌞 🌤️ 🌈
```

Or import the helper:

```python
from src.forecast import get_forecast
print(get_forecast())
```

## How it works

The utility hashes the current date (or a supplied `datetime.date`) to produce a deterministic pseudo‑random selection of weather‑related emojis. The same date always yields the same forecast, making it safe for offline, repeatable tests.
