# Nightly Emoji Forecast

A tiny utility that prints a whimsical emoji weather forecast for a given date. Useful for adding a dash of fun to README files, Slack messages, or commit logs.

## Usage

```bash
python -m emoji_forecast 2023-10-31   # prints forecast for given date
python -m emoji_forecast               # prints forecast for today
```

## How it works

The forecast is deterministic: it maps the day of the year to one of six emojis, so the same date always yields the same result.
