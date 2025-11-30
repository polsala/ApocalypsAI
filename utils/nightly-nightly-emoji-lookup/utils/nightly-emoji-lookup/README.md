# Nightly Emoji Lookup

Utility to retrieve the official CLDR short name for a given emoji character.

## Features
- **Zero external dependencies** – just the Python standard library.
- Provides a programmatic API `get_name(emoji: str) -> str | None`.
- Comes with a tiny CLI: `python -m emoji_lookup "🚀"` prints `rocket`.
- Fully tested offline with deterministic mock data.

## Usage (Python)
```python
from emoji_lookup import get_name

print(get_name("😀"))  # → "grinning face"
print(get_name("🦄"))  # → None (unknown in built‑in map)
```

## Usage (CLI)
```bash
$ python -m emoji_lookup "🚀"
rocket
```

## Extending the map
Edit `src/emoji_lookup.py` and add entries to the `EMOJI_MAP` dictionary.
