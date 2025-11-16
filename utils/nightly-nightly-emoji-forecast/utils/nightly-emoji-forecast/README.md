# Nightly Emoji Forecast

A tiny utility that generates a whimsical emoji weather forecast for any given date. Perfect for adding a splash of fun to daily stand‑ups, README badges, or chat bots.

## Features

- **Deterministic** – the same date always yields the same forecast.
- **Zero dependencies** – pure Python 3.11.
- **CLI** – `python -m nightly-emoji-forecast` prints today’s forecast.
- **Library** – import `get_forecast(date)`.

## Usage

```bash
# CLI (prints today’s forecast)
python -m nightly-emoji-forecast

# Library
from nightly_emoji_forecast import get_forecast
import datetime
print(get_forecast(datetime.date(2025, 1, 1)))
```

## How it works

The utility hashes the ISO‑formatted date and maps the result to a short sequence of emojis representing sun, clouds, rain, thunder, snow, and more.

## Tests

Run the test suite with **pytest**:

```bash
cd utils/nightly-emoji-forecast
pytest -q
```
