# Nightly Hex‑Color Converter

Convert between CSS‑style hexadecimal colour codes (e.g. `#ff00aa`) and RGB tuples (`(255, 0, 170)`).

## Features

- **Library functions** `hex_to_rgb` and `rgb_to_hex` for programmatic use.
- **Command‑line interface** for quick on‑the‑fly conversion.
- Zero external dependencies – pure Python 3.11 standard library.

## Installation

The utility is self‑contained. Copy the `src/` directory into your project or run it directly from the repository:

```bash
python -m utils.hex-color-converter.src.converter --help
```

## Usage

### Library

```python
from utils.hex-color-converter.src.converter import hex_to_rgb, rgb_to_hex

print(hex_to_rgb("#ff00aa"))   # (255, 0, 170)
print(rgb_to_hex((255, 0, 170))) # "#ff00aa"
```

### CLI

```bash
# Hex → RGB
python -m utils.hex-color-converter.src.converter --hex "#1e90ff"
# Output: (30, 144, 255)

# RGB → Hex
python -m utils.hex-color-converter.src.converter --rgb 30 144 255
# Output: #1e90ff
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/nightly-hex-color-converter/utils/hex-color-converter/tests
```
