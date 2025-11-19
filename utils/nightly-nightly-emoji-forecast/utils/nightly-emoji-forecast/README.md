# Nightly Emoji Forecast

A tiny utility that provides a deterministic “weather” forecast expressed as an emoji for any given date. Perfect for adding a splash of fun to daily stand‑ups, commit messages, or Slack bots.

## Usage

```bash
python -m utils.nightly_emoji_forecast.src.forecast [--date YYYY-MM-DD]
```

- If `--date` is omitted, today’s date is used.
- The forecast is deterministic: the same date always yields the same emoji.

## How it works

The date string is hashed with SHA‑256, the resulting integer is taken modulo the number of available emojis, and the corresponding emoji is returned.

## Available emojis

☀️ 🌤️ ⛅ 🌥️ ☁️ 🌧️ ⛈️ ❄️ 🌪️ 🌈
