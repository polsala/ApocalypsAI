# Nightly Emoji Weather Forecast

Utility that converts plain‑language weather descriptions into corresponding emojis. Handy for adding a splash of fun to logs, messages, or markdown reports.

## Usage

```bash
python -m utils.nightly_emoji_weather_forecast.src.emoji_forecast "light rain"
# Output: 🌧️
```

## Mapping

- **sunny**, **clear** → ☀️
- **partly cloudy**, **cloudy** → 🌤️
- **rain**, **drizzle**, **light rain** → 🌧️
- **thunderstorm**, **storm** → ⛈️
- **snow**, **flurries** → ❄️
- **fog**, **mist** → 🌫️
- any other description → ❓

## Tests

Run with `pytest`:

```bash
pytest -q utils/nightly-emoji-weather-forecast/tests
```
