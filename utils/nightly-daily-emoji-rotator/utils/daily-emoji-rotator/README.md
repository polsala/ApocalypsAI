# Daily Emoji Rotator

A whimsical‑yet‑useful utility that returns a *deterministic* emoji for the current day.

## Features
- No external network calls – works completely offline.
- Deterministic: the same date always yields the same emoji.
- Tiny dependency footprint (standard library only).
- Provides a CLI entry‑point (`python -m daily_emoji_rotator`) and a reusable Python function.

## Usage
```bash
# Print today’s emoji
python -m daily_emoji_rotator
```

Or import in your own code:
```python
from daily_emoji_rotator import get_today_emoji
print(get_today_emoji())
```

## How it works
The utility hashes the ISO‑format date (`YYYY‑MM‑DD`) and maps the hash to an index in a curated emoji list. Because the hash is deterministic, the same date always maps to the same emoji.

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/daily-emoji-rotator/utils/daily-emoji-rotator/tests
```
