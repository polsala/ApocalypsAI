# Emoji Forecast

A tiny utility that returns a whimsical emoji representing the "weather" for any given date. Perfect for adding a splash of fun to logs, commit messages, or chat bots.

## Usage

```bash
python -m utils.nightly-emoji-forecast.src.forecast   # prints today's forecast
python -m utils.nightly-emoji-forecast.src.forecast 2023-01-01   # prints forecast for specific date
```

## API

```python
from utils.nightly-emoji-forecast.src.forecast import get_forecast
forecast = get_forecast(date)  # date is a datetime.date
```

## How it works

The forecast is deterministic: it hashes the date to an index in a fixed list of emojis, so the same date always yields the same emoji.
