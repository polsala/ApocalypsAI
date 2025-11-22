# Nightly Emoji Forecast

A tiny, self‑contained utility that returns a single emoji representing a *pretend* weather forecast for a supplied date.

## Why?
- Adds a dash of fun to CI logs, daily stand‑ups, or commit messages.
- Completely deterministic – the same date always yields the same emoji.
- Zero external dependencies; pure Python 3.11.

## Usage
```bash
python -m utils.nightly-emoji-forecast.src.forecast 2025-12-25
# → 🌨️ (example)
```
Or import in your own code:
```python
from utils.nightly-emoji-forecast.src.forecast import get_forecast
import datetime
print(get_forecast(datetime.date.today()))
```

## Implementation Details
- The function seeds a `random.Random` instance with the ISO ordinal of the date, then picks an emoji from a fixed list.
- Determinism makes it safe for automated tests and offline environments.

## Testing
Run the bundled tests with:
```bash
python -m unittest discover utils/nightly-emoji-forecast/tests
```
