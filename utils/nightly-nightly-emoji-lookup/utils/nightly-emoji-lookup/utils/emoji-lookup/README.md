# Emoji Lookup Utility

`emoji-lookup` provides a simple, dependency‑free way to translate a short, human‑readable name into its corresponding Unicode emoji.

## Features
- **Zero external dependencies** – pure Python standard library.
- **Deterministic & offline** – the mapping is baked into the source.
- **CLI & library usage** – import `get_emoji` in your code or run the tiny command‑line helper.

## Installation
Copy the `utils/nightly-emoji-lookup` folder into your project or install it as a submodule. No `pip` install required.

## Usage
### As a library
```python
from utils.emoji_lookup.src.lookup import get_emoji

print(get_emoji("thumbs_up"))  # ➜ 👍
```

### As a CLI
```bash
python -m utils.emoji_lookup.src.lookup thumbs_up
# Output: 👍
```

## Extending the map
Edit `EMOJI_MAP` in `src/lookup.py` to add or override entries.
