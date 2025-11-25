# Nightly Hex Colour Generator

A whimsical yet handy command‑line tool that spits out a random hex colour code (e.g. `#3FA7C9`).

## Features

- **Random colour generation** using Python's standard `random` module.
- **Optional seed** for reproducible output – perfect for tests or deterministic scripts.
- **Brightness classification** (`light`, `dark`, or `neutral`).
- Zero external dependencies; works with the default Python 3.11 runtime.

## Installation & Usage

```bash
# Clone the repository (or copy the folder) and navigate into it
cd utils/nightly-hex-color-generator

# Run the utility directly
python -m src.generator          # → prints a random colour, e.g. #A1B2C3
python -m src.generator --seed 42 # → deterministic colour
```

## API

```python
from src.generator import generate_color, classify_brightness

hex_code = generate_color()               # random colour
hex_code = generate_color(seed=123)       # deterministic colour
brightness = classify_brightness(hex_code)  # 'light' | 'dark' | 'neutral'
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s tests
```

All tests are offline and deterministic – they mock the random number generator.
