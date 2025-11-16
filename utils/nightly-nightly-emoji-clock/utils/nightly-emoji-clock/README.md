# Nightly Emoji Clock

A tiny, self‑contained Python utility that turns a 24‑hour time into the matching clock‑face emoji.

## Features

- `get_clock_emoji(hour: int, minute: int) -> str`
- Rounds minutes to the nearest half‑hour (0 or 30).
- Handles wrap‑around at midnight.
- No external dependencies – pure standard library.

## Usage

```python
from src.emoji_clock import get_clock_emoji

print(get_clock_emoji(14, 22))  # → 🕑 (2 o’clock)
print(get_clock_emoji(9, 45))   # → 🕙 (10 o’clock, rounded up)
```

## Why?

Adding a visual cue to timestamps can make logs or commit messages more readable and fun, while still being deterministic and offline.
