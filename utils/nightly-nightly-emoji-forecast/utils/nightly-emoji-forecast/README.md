# Nightly Emoji Forecast

A whimsical utility that generates a deterministic emoji weather forecast for any given date. Perfect for adding a splash of fun to daily stand‑ups, commit messages, or Slack bots.

## How it works

The forecast is derived from a simple hash of the ISO‑formatted date, mapping to a fixed list of weather emojis. Because the algorithm is deterministic, the same date always yields the same emoji, making it safe for offline testing.

## Usage

```bash
python -m src.forecast 2025-12-03
# => 🌦️
```

Or import in Python:

```python
from src.forecast import get_emoji_forecast
print(get_emoji_forecast(date.today()))
```

## Testing

Run the test suite with:

```bash
python -m unittest discover -s tests
```
