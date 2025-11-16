# Emoji Clock

A whimsical utility that converts a given time into clock‑face emojis. Useful for adding a fun visual representation of timestamps in logs, commit messages, or chat.

## Usage

```bash
python -m emoji_clock 14:23
# 🕑🕝
```

The utility rounds minutes to the nearest 5 minutes and selects the appropriate minute‑hand emoji.

## API

```python
from datetime import datetime
from src.emoji_clock import time_to_emoji

now = datetime.now()
print(time_to_emoji(now))
```

`time_to_emoji(dt: datetime) -> str`

Returns a string of two emojis: the hour‑hand emoji and the minute‑hand emoji.

## Tests

Run the test suite with:

```bash
pytest -q
```

The tests are deterministic and require no external resources.
