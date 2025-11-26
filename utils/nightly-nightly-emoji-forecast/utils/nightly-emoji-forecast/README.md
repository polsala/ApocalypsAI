# Nightly Emoji Forecast

A tiny utility that produces a whimsical emoji "weather forecast" for any given date. Perfect for adding a splash of fun to daily stand‑ups, commit messages, or Slack updates.

## Usage

```bash
python -m nightly_emoji_forecast src/forecast.py [YYYY-MM-DD]
```

If no date is supplied, it uses today’s date.

## How it works

The forecast is deterministic and offline:
1. Compute the sum of the year, month, and day.
2. Take the remainder modulo the number of available emojis.
3. Return the emoji at that index.

## Testing

Run the tests with:

```bash
pytest -q
```
