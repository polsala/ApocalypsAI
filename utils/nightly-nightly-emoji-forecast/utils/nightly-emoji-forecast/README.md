# Nightly Emoji Forecast

A whimsical utility that generates a deterministic daily emoji forecast based on the current date. Perfect for adding a splash of fun to your terminal or CI logs.

## Usage

```bash
python -m forecast
# 🌞
```

Or import:

```python
from forecast import get_forecast
print(get_forecast())
```

The forecast is deterministic: the same date always yields the same emoji.

## Implementation

Uses a small list of weather‑related emojis and seeds Python's `random` with the ISO date string.
