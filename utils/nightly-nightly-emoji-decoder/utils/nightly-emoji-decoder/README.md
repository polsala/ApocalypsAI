# Nightly Emoji Decoder

A whimsical yet useful utility that converts a string of emojis into a readable English phrase.

## Features
- Built‑in emoji‑to‑word dictionary.
- Simple `decode` function for programmatic use.
- Command‑line interface for quick decoding.

## Usage
```bash
python -m src.decoder "🚀🌕"
# Output: "rocket moon"
```

Or in Python:
```python
from src.decoder import decode
print(decode("🧩🔧"))  # -> "puzzle wrench"
```

## Extending
Edit the `_EMOJI_MAP` dictionary in `src/decoder.py` to add or change mappings.
