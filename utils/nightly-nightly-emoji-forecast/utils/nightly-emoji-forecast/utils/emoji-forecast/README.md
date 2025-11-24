# Emoji Forecast

A tiny utility that returns a whimsical emoji representing the weather forecast for a given date. No network calls; uses deterministic pseudo‑random mapping based on the date string.

## Usage

```bash
python -m emoji_forecast src/forecast.py 2025-01-01
# 🌞
```

Or import:

```python
from emoji_forecast import get_emoji_forecast
print(get_emoji_forecast("2025-01-01"))
```

## How it works

It hashes the ISO date string, takes modulo over a list of weather emojis, and returns the selected emoji. This ensures the same date always yields the same emoji.
