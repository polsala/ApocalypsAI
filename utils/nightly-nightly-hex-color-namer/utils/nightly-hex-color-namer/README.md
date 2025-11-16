# Hex Color Namer

Utility to translate hex color codes (e.g., `#ff0000`) into human‑readable basic color names. It uses a small built‑in palette of common colors and picks the nearest one by Euclidean distance in RGB space.

## Usage

```bash
python -m utils.nightly-hex-color-namer.src.color_namer "#00ff00"
# => lime
```

## API

```python
hex_to_name(hex_code: str) -> str
```

Returns the name of the nearest color, or `"unknown"` if the input is invalid.

## Tests

Run with `pytest`:

```bash
cd utils/nightly-hex-color-namer
pytest -q
```
