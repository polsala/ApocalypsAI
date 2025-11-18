# Emoji Clock Utility

Convert a time of day into the nearest clock‑face emoji (hour or half‑hour). Useful for adding a visual time cue to messages, logs, or markdown.

## Usage

```bash
python -m utils.nightly-emoji-clock.src.emoji_clock 13:45
# → 🕑
```

(13:45 rounds to 14:00 → 🕑)

## API

```python
from utils.nightly-emoji-clock.src.emoji_clock import time_to_emoji

emoji = time_to_emoji("09:20")  # "🕥"
```

## Installation

The utility is self‑contained; just run the script with Python 3.11.
