# Emoji Forecast

A tiny utility that provides a deterministic daily emoji "weather" forecast. Useful for adding a splash of fun to logs, commit messages, or daily stand‑ups.

## Usage

```bash
python -m forecast
# or
from forecast import get_daily_emoji
print(get_daily_emoji())
```

The forecast is based on the day of year, so it's repeatable.

## How it works

It maps the day of year modulo a short list of emojis representing weather moods. No external data or network calls are required.
