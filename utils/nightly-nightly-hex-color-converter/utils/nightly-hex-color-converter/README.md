# Nightly Hex Color Converter

A whimsical yet handy utility that converts colors between the common hexadecimal string format (e.g., `#ff00aa`) and an RGB tuple `(255, 0, 170)`.  It ships with a tiny command‑line interface and a full test suite.

## Features

- `hex_to_rgb(hex_str) → (r, g, b)`
- `rgb_to_hex(r, g, b) → "#rrggbb"`
- Simple CLI: `python -m color_converter <hex|rgb> <value>`

## Installation & Usage

The utility is self‑contained; just copy the `src/` directory into your project or run it directly:

```bash
python -m utils/nightly-hex-color-converter/src/color_converter hex #ff00aa
# => (255, 0, 170)

python -m utils/nightly-hex-color-converter/src/color_converter rgb 255 0 170
# => #ff00aa
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover utils/nightly-hex-color-converter/tests
```

---

*Created by the ApocalypsAI Nightly Integrator.*
