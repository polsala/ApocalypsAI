# Nightly Emoji Lookup

Utility to translate between emoji shortcodes (e.g., `:smile:`) and their Unicode characters. Provides a tiny CLI and a Python API.

## Features

- `name_to_emoji(":smile:")` → "😄"
- `emoji_to_name("😄")` → ":smile:"
- List all supported mappings.
- Command‑line usage:
  ```bash
  python -m utils/nightly-emoji-lookup/src/emoji_lookup.py --to-emoji ":heart:"
  # => ❤️
  ```

## Installation

Copy the folder into your repository. No external dependencies beyond the Python standard library.

## Usage (Python API)

```python
from emoji_lookup import name_to_emoji, emoji_to_name, list_all

print(name_to_emoji(":thumbs_up:"))  # 👍
print(emoji_to_name("🔥"))            # :fire:
print(list_all())                     # {':smile:': '😄', ...}
```

## Usage (CLI)

```bash
# Convert shortcode to emoji
python -m utils/nightly-emoji-lookup/src/emoji_lookup.py --to-emoji ":thumbs_up:"

# Convert emoji to shortcode
python -m utils/nightly-emoji-lookup/src/emoji_lookup.py --to-name "❤️"

# List all mappings
python -m utils/nightly-emoji-lookup/src/emoji_lookup.py --list
```
