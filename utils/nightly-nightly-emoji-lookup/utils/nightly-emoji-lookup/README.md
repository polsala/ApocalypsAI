# Nightly Emoji Lookup

Utility to translate between emoji shortcodes (e.g., `:smile:`) and Unicode emoji characters. Works completely offline – no network calls, no external dependencies.

## Features
- Convert a shortcode to its emoji.
- Convert an emoji to its shortcode.
- Small built‑in mapping that can be extended.

## Installation
```bash
# The utility is self‑contained; just copy the folder or install via pip if you wish.
# No extra packages are required.
```

## Usage
```bash
# Convert shortcode to emoji
python -m src.emoji_lookup --to-emoji ":smile:"
# => 😄

# Convert emoji to shortcode
python -m src.emoji_lookup --to-shortcode "😄"
# => :smile:
```

## Extending the Mapping
Edit `src/emoji_lookup.py` and add entries to the `_EMOJI_MAP` dictionary.

## Testing
```bash
python -m unittest discover -s tests
```
