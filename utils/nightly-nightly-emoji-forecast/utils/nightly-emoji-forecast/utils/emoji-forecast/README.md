# Emoji Forecast

A whimsical utility that gives you a deterministic emoji "weather" forecast for any given date. Useful for adding a daily mood icon to logs, commit messages, or chat.

## Usage

```bash
python -m forecast 2025-12-01
# 🌧️
```

Or import in Python:

```python
from forecast import get_emoji_for_date
emoji = get_emoji_for_date(date(2025, 12, 1))
```

## How it works

The forecast is deterministic: it hashes the ISO calendar day (YYYY‑MM‑DD) to an index in a fixed list of emojis, so the same date always yields the same emoji without any network calls.
