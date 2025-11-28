# Emoji Forecast

A tiny utility that converts simple weather data into an emoji‑based forecast. Perfect for adding a splash of fun to daily stand‑ups or chat bots.

## Usage

```bash
python -m emoji_forecast path/to/weather.json
```

The JSON should contain keys `temperature`, `condition` (e.g., `"sunny"`, `"rainy"`, `"cloudy"`, `"snow"`).

The script prints an emoji line like:

```
🌞 23°C – Good day!
```

## Tests

Run with `pytest`:

```bash
pytest
```
