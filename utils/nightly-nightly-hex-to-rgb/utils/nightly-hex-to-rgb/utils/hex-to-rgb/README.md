# Hex to RGB Converter

Utility that converts a hex colour string (e.g., `#ff00aa` or `ff00aa`) into an RGB tuple of integers. Includes a small CLI for quick conversion.

## Usage

```bash
python -m utils.hex_to_rgb src/hex_to_rgb.py "#ff00aa"
# Output: (255, 0, 170)
```

## API

```python
from utils.hex_to_rgb.src.hex_to_rgb import hex_to_rgb

rgb = hex_to_rgb("#ff00aa")  # -> (255, 0, 170)
```

## Tests

Run with `pytest`:

```bash
pytest utils/nightly-hex-to-rgb/utils/hex-to-rgb/tests
```
