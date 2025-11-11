# Emoji Lookup Utility

Provides functions to convert between emoji shortcodes (e.g., `:smile:`) and their Unicode characters. Includes a small CLI for quick lookups.

## Usage

```bash
python -m emoji_lookup.lookup --to-emoji smile
# 😄

python -m emoji_lookup.lookup --to-name 😄
# smile
```

## API

- `name_to_emoji(name: str) -> str | None`
- `emoji_to_name(emoji: str) -> str | None`
