# Emoji Forecast

A tiny utility that provides a whimsical emoji weather forecast for a given date. No external API; uses deterministic pseudo‑random based on the date, so results are repeatable and offline.

## Usage

```bash
python -m src.forecast 2025-12-25
# Output: 🌧️☔️🌈
```

## API

`get_emoji_forecast(date_str: str) -> str`

Returns a string of emojis representing the forecast.
