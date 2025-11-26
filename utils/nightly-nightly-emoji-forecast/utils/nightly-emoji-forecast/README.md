# Nightly Emoji Forecast

## Overview
`nightly-emoji-forecast` is a tiny, self‑contained Python utility that returns a playful emoji "weather" forecast for any date you provide. The forecast is **deterministic** – the same date always yields the same emoji – making it perfect for:

- Adding a daily mood icon to Slack/Discord messages.
- Decorating logs or CI run summaries with a fun symbol.
- Generating whimsical placeholders in documentation.

## How it works
The utility hashes the ISO‑format date string (`YYYY‑MM‑DD`) and maps the resulting integer to one of five emojis:

| Emoji | Meaning |
|-------|---------|
| 🌞   | Sunny   |
| 🌦️   | Partly Cloudy |
| 🌧️   | Rainy |
| ❄️   | Snowy |
| 🌪️   | Stormy |

Because the mapping uses a simple modulo operation, the output is fully deterministic and requires **no external services**.

## Usage
```bash
# Run as a module
python -m utils.nightly-emoji-forecast.src.emoji_forecast 2025-12-31
# => 🌪️
```

Or import in your own code:
```python
from utils.nightly-emoji-forecast.src.emoji_forecast import get_forecast
print(get_forecast("2025-12-31"))  # 🌪️
```

## Testing
Run the tests with:
```bash
python -m unittest discover utils/nightly-emoji-forecast/tests
```
All tests are deterministic and offline.
