# Hex Color Namer

Utility to convert a hex color (e.g., `#ff0000`) to the nearest common color name (e.g., `red`). Includes a small built‑in palette of 16 basic colors and can be extended.

## Installation

```bash
# No external dependencies – just run the script directly
python -m nightly_hex_color_namer.src.namer "#ff00ff"
```

## Usage

```bash
python -m nightly_hex_color_namer.src.namer "#00ff00"
# Output: lime
```

## API

```python
from nightly_hex_color_namer.src.namer import get_color_name

name = get_color_name("#ff0000")  # → "red"
```

## Testing

```bash
pytest -q
```
