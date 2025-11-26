# Hex Color Namer

Utility that turns a hex color code (e.g., `#ff5733`) into a whimsical, deterministic name like `vivid ember`. No external APIs; works offline.

## Installation

Copy the folder into your repository. Requires Python 3.11.

## Usage

```bash
python -m utils.nightly_hex_color_namer.src.color_namer "#ff5733"
# Output: vivid ember
```

Or import the function directly:

```python
from utils.nightly_hex_color_namer.src.color_namer import name_color
print(name_color("#ff5733"))
```

## How it works

- Strips an optional leading `#`.
- Converts the hex string to an integer.
- Uses two word lists (adjectives & nouns) and modulo arithmetic to pick words.
- Deterministic: the same input always yields the same name.

## Testing

Run the tests with `pytest` inside the utility folder:

```bash
cd utils/nightly-hex-color-namer
pytest -q
```
