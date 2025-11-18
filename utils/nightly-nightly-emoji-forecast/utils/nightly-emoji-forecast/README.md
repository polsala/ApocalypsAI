# Nightly Emoji Forecast

A tiny, self‑contained Python utility that turns a calendar date into a playful weather forecast expressed entirely in emojis.

## Features
- **Zero external dependencies** – pure standard library.
- **Deterministic** – the same date always yields the same forecast.
- **CLI & library** – use it from the command line or import the `get_emoji_forecast` function.

## Installation
```bash
# From the repository root
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt  # (no extra deps needed)
```

## Usage
```bash
python -m utils/nightly-emoji-forecast/src/forecast 2025-12-25
# → 🌨️
```

Or as a library:
```python
from utils.nightly-emoji-forecast.src.forecast import get_emoji_forecast
import datetime
print(get_emoji_forecast(datetime.date.today()))
```

## Testing
```bash
pytest utils/nightly-emoji-forecast/tests
```

## How it works
The utility hashes the ISO‑formatted date string, takes the modulo of the number of available emojis, and selects the corresponding emoji. This guarantees repeatability without any network calls.
