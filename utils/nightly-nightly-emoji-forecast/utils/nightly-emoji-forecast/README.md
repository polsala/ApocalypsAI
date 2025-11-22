# Nightly Emoji Forecast

A tiny utility that produces a deterministic "emoji forecast" for any given day. The forecast is derived from the day‑of‑year and a curated list of emojis, making it reproducible and completely offline.

## Features
- Pure Python 3.11, no external dependencies.
- Deterministic output – the same date always yields the same emoji.
- Simple CLI for quick use in scripts or terminals.
- Comprehensive unit tests with mocked dates.

## Usage
```bash
python -m utils.nightly-emoji-forecast.src.forecast          # forecast for today
python -m utils.nightly-emoji-forecast.src.forecast 2025-12-25  # forecast for a specific date
```

## API
```python
from utils.nightly-emoji-forecast.src.forecast import get_emoji_forecast

emoji = get_emoji_forecast(date)  # `date` is a datetime.date instance
```

## Testing
Run the tests with:
```bash
python -m unittest discover utils/nightly-emoji-forecast/tests
```
