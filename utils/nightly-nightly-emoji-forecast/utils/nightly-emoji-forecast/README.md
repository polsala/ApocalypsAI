# Nightly Emoji Forecast

A whimsical utility that generates a deterministic emoji weather forecast for any given date. Perfect for adding a splash of fun to daily stand‑ups, commit messages, or Slack updates.

## How it works

The forecast is derived from the calendar date using a simple arithmetic formula, then mapped onto a short sequence of weather‑related emojis (☀️, 🌤️, ⛅, 🌥️, ☁️, 🌦️, 🌧️, ⛈️, ❄️, 🌪️, 🌈, 🌫️). Because the algorithm is deterministic, the same date always yields the same forecast.

## Usage

```bash
python -m utils.nightly-emoji-forecast.src.forecast 2025-11-16
# => 🌤️🌦️☀️
```

Or import in Python:

```python
from utils.nightly_emoji_forecast.src.forecast import get_forecast
from datetime import date
print(get_forecast(date(2025, 11, 16)))
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/nightly-emoji-forecast/tests
```
