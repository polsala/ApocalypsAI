# Emoji Forecast

A tiny utility that generates a deterministic weather forecast represented by emojis for any given date. Perfect for adding a splash of fun to your daily scripts or commit messages.

## Usage

```bash
python -m emoji_forecast src/forecast.py [YYYY-MM-DD]
```

If no date is provided, today’s date is used.

## How it works

The forecast is based on the day of the year modulo 4, mapping to four weather types:

- 0 → ☀️ Sunny
- 1 → ☁️ Cloudy
- 2 → 🌧️ Rainy
- 3 → ❄️ Snowy

The algorithm is deterministic and requires no external data.

## Testing

Run the tests with:

```bash
python -m unittest discover -s utils/nightly-emoji-forecast/utils/emoji-forecast/tests
```
