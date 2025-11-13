# Emoji Time‑Ago Utility

`emoji-time-ago` turns an ISO‑8601 timestamp into a friendly "X minutes ago" (or "X days ago") string, prefixed with an emoji that hints at the elapsed magnitude.

## Features

- Pure Python 3.11, no external dependencies.
- Library function `format_time_ago(timestamp: str, now: datetime | None = None) -> str`.
- Small CLI wrapper (`python -m emoji_time_ago <timestamp>`).
- Deterministic offline test suite.

## Usage

```bash
# As a module
python -m emoji_time_ago 2025-11-13T10:30:00Z
# => 📅 2 days ago

# In code
from src.emoji_time_ago import format_time_ago
print(format_time_ago("2025-11-13T10:30:00Z"))
```

## Emoji Scale

| Elapsed | Emoji |
|---------|-------|
| < 1 minute | ⏱️ |
| < 1 hour   | 🕒 |
| < 1 day    | 🌅 |
| < 7 days   | 📅 |
| ≥ 7 days   | 📆 |

## Testing

Run the test suite with:

```bash
python -m unittest discover -s utils/emoji-time-ago/tests
```
