# Nightly Emoji Forecast

A whimsical utility that gives you a daily emoji forecast based on the date. Perfect for adding a splash of fun to your terminal, commit messages, or daily stand‑ups.

## How it works

- Weekdays map to a base emoji.
- The month adds a subtle modifier.
- The final emoji is deterministic and offline.

## Usage

```bash
python -m utils.nightly-emoji-forecast.src.forecast
# or
python utils/nightly-emoji-forecast/src/forecast.py
```

Outputs today's emoji.

## API

```python
from datetime import date
from utils.nightly-emoji-forecast.src.forecast import get_daily_emoji

emoji = get_daily_emoji(date(2025, 11, 16))
```
