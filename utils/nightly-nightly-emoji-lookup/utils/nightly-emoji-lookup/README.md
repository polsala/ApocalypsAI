# Nightly Emoji Lookup

**Utility name:** `nightly-emoji-lookup`

## What it does

Provides a fast, offline lookup from a keyword (e.g. `rocket`, `coffee`) to the matching Unicode emoji. The mapping is stored in a small built‑in dictionary, so no network calls are required.

## Usage

```bash
python -m utils.nightly-emoji-lookup.src.emoji_lookup <keyword>
```

The script prints the emoji if found, otherwise prints an empty string.

You can also import the function in your own Python code:

```python
from utils.nightly-emoji-lookup.src.emoji_lookup import get_emoji

print(get_emoji("rocket"))  # 🚀
```

## Extending the dictionary

Edit `src/emoji_lookup.py` and add entries to the `_EMOJI_MAP` dictionary. The keys are case‑insensitive.

## Testing

Run the tests with:

```bash
python -m pytest utils/nightly-emoji-lookup/tests
```

---

*This utility is deliberately lightweight and has **zero external dependencies**, making it safe for the nightly self‑heal workflow.*
