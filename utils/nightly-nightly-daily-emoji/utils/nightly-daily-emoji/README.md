# nightly-daily-emoji

## Summary
Generates a deterministic emoji for any given date. The emoji is derived from a SHA‑256 hash of the ISO‑8601 date string, ensuring the same date always maps to the same emoji. Perfect for adding a whimsical daily marker to commit messages, logs, or journal entries.

## Usage
```python
from daily_emoji import get_daily_emoji

emoji = get_daily_emoji("2025-11-14")
print(emoji)  # e.g., "🌟"
```

## How it works
1. Accepts a date string (`YYYY‑MM‑DD`).
2. Computes SHA‑256 of the string.
3. Uses the first few bits to index into a curated list of 30 emojis.

## CLI (optional)
```bash
python -m daily_emoji 2025-11-14
# 🌟
```

## Testing
Run `pytest -q` inside the utility folder.
