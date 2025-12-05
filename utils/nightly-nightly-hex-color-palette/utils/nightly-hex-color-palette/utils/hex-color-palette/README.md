# Hex Color Palette Generator

Utility to generate a list of random hex color codes. Useful for designers, terminal themes, and any situation where a quick palette is needed.

## Features
- Generate any number of colors.
- Optional seed for reproducible palettes.
- Simple CLI: `python -m src.palette <count> [--seed <int>]`.

## Installation
```bash
cd utils/nightly-hex-color-palette/utils/hex-color-palette
python -m venv .venv
source .venv/bin/activate
# No external dependencies required
```

## Usage
```bash
python -m src.palette 5 --seed 42
```

## Testing
```bash
python -m unittest discover -s tests
```
