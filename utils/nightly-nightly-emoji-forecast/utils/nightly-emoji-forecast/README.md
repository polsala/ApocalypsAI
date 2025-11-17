# Nightly Emoji Forecast

A tiny, self‑contained utility that turns a calendar date into a pair of emojis – one representing the weather and one representing the mood. The mapping is **deterministic** (based on a SHA‑256 hash of the date) and requires no network access.

## Usage

```bash
python -m src.forecast 2025-12-31
# Example output: 🌨️🤔
```

The utility is pure Python 3.11 and can be imported in other projects:

```python
from src.forecast import get_forecast
import datetime

print(get_forecast(datetime.date.today()))
```

## How it works

1. The date string (`YYYY‑MM‑DD`) is combined with a prefix (`weather-` or `mood-`).
2. A SHA‑256 hash is computed and reduced modulo the length of the emoji list.
3. The selected weather and mood emojis are concatenated and returned.

## Testing

Run the test suite with `pytest`:

```bash
pytest -q utils/nightly-emoji-forecast/tests
```
