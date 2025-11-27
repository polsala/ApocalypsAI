# Nightly Emoji Forecast

A tiny, self‑contained Python utility that returns a playful weather forecast expressed entirely in emojis.

## Features

- **Deterministic**: The same date always yields the same forecast, making tests reliable and offline.
- **Zero external dependencies** – only the Python standard library.
- **CLI & library usage** – import `get_forecast` in your code or run the module directly.

## Usage

```bash
# As a script (defaults to today)
python -m nightly-emoji-forecast

# Specify a date (YYYY‑MM‑DD)
python -m nightly-emoji-forecast 2025-12-31
```

```python
from nightly_emoji_forecast.src.forecast import get_forecast
import datetime

print(get_forecast(datetime.date.today()))
```

## How it works

The forecast is derived from the day‑of‑year modulo a curated list of weather‑related emojis. This ensures:

1. **Predictability** – no network calls, no randomness.
2. **Whimsy** – a rotating palette of sun, clouds, rain, snow, thunder, etc.

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/nightly-emoji-forecast/tests
```

---

*Created by the ApocalypsAI Nightly Integrator.*
