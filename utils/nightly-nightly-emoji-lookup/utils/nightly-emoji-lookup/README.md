# Nightly Emoji Lookup

Utility to map plain English keywords to emojis. Useful for adding flair to messages, logs, or documentation.

## Features
- **Pure Python 3.11** – no external dependencies.
- **Static dictionary** – works offline, deterministic.
- **CLI** – `python -m emoji_lookup <keyword>` prints the matching emoji.
- **Library function** – `get_emoji(keyword: str) -> str` for programmatic use.

## Usage
```bash
# As a module
python -m emoji_lookup fire
# => 🔥

# In code
from src.emoji_lookup import get_emoji
print(get_emoji("rocket"))  # 🚀
```

## Extending
Add new mappings to the `_EMOJI_MAP` dictionary in `src/emoji_lookup.py`.
