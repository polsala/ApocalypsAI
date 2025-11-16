# Nightly Hex Color Namer

A tiny utility that translates a hex color code (e.g., `#ff5733`) into the nearest common color name (e.g., `orange`). It uses a small built‑in palette of 16 basic colors and picks the one with the smallest Euclidean distance in RGB space.

## Installation

The utility is pure Python 3.11 and has no external dependencies.

```bash
cd utils/nightly-hex-color-namer
python -m venv .venv
source .venv/bin/activate
pip install .
```

## Usage

```bash
python -m src.hex_color_namer "#ff5733"
# => orange
```

## Testing

```bash
pytest -q
```

## How it works

1. Parse the hex string into RGB components.
2. Compute Euclidean distance to each palette entry.
3. Return the name of the closest match.

The palette is deliberately tiny to keep the utility lightweight and whimsical.
