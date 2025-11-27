# Nightly Colorful Hex Namer

Utility that translates a hex colour code (e.g., `#ff5733`) into a whimsical, human‑readable name (e.g., `Sunset Blaze`). Useful for designers, developers, or anyone who prefers words over raw numbers.

## Usage

```sh
python -m src.hex_namer "#ff5733"
# => Sunset Blaze
```

Or import the function:

```python
from src.hex_namer import name_from_hex
print(name_from_hex("#1a2b3c"))
```

## How it works

The script extracts the red, green, and blue components, then matches them against a tiny handcrafted palette of 12 whimsical names.

## Tests

Run with `pytest`:

```sh
pytest -q
```
