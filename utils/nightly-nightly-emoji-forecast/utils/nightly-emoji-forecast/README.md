# Nightly Emoji Forecast

**What it does**

- Generates a simple, deterministic "weather" forecast for any given date.
- Returns one of four emojis: ☀️ (sunny), 🌤️ (partly cloudy), 🌧️ (rainy), ❄️ (snowy).
- Can be used as a CLI (`python -m forecast`) to print today’s forecast or imported as a library.

**Why it’s useful**

- Adds a whimsical, yet predictable, element to daily communications.
- No external APIs, network calls, or randomness – perfect for offline CI environments.

**Usage**

```bash
# As a module (prints today’s forecast)
python -m utils.nightly-emoji-forecast.src.forecast

# As a library
>>> from utils.nightly-emoji-forecast.src.forecast import get_forecast
>>> get_forecast(date(2025, 12, 25))
'❄️'
```

**Implementation notes**

- The forecast is derived from the ISO week number and weekday, ensuring the same input date always yields the same emoji.
- No third‑party dependencies; only the Python standard library.
