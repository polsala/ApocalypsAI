# Nightly Hex Color Namer

Utility that translates a hex color code (e.g., `#FF5733`) into a whimsical, human‑readable name. Useful for logs, UI theming, or just adding personality to scripts.

## Usage

```bash
python -m src.color_namer "#ff5733"
# => "Fiery Tangerine"
```

You can also import the function in your own code:

```python
from src.color_namer import get_color_name
name = get_color_name("#ff5733")
```

## How it works

A small built‑in lookup table maps common colors to fun names. If the exact code isn’t in the table, the utility falls back to a deterministic pseudo‑name based on the hue of the color.

## Tests

Run the test suite with:

```bash
python -m unittest discover -s tests
```
