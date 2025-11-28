# Nightly Emoji Clock

Utility that converts a given time (or the current local time) into the corresponding clock face emoji. Useful for adding a whimsical timestamp to logs, messages, or markdown.

## Features

- `get_clock_emoji(dt)` returns the appropriate emoji for any `datetime`.
- CLI `python -m src.emoji_clock` prints the emoji for the current time.
- No external dependencies; pure Python 3.11.

## Installation

Copy the folder into your repo and run the tests with `python -m unittest`.

## Usage

```python
from src.emoji_clock import get_clock_emoji
from datetime import datetime

emoji = get_clock_emoji(datetime(2023, 1, 1, 14, 30))
print(emoji)  # 🕑
```

CLI:

```bash
$ python -m src.emoji_clock
🕓
```
