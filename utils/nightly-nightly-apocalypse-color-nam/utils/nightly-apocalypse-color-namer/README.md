# Nightly Apocalypse Color Namer

**Utility name:** `nightly-apocalypse-color-namer`

## Overview

`nightly-apocalypse-color-namer` turns a standard hexadecimal color code (e.g., `#ff5733`) into a whimsical, post‑apocalyptic name such as **"Radiant Wasteland"**. The mapping is fully deterministic and requires no external services, making it safe for offline use and CI pipelines.

## Features

- Pure‑Python implementation (Python 3.11 compatible).
- No third‑party dependencies beyond the standard library.
- Deterministic name generation based on the numeric value of the hex code.
- Simple validation of input format.

## Usage

```bash
python -m utils.nightly-apocalypse-color-namer.src.color_namer <hex_code>
```

Or import the function in your own code:

```python
from utils.nightly-apocalypse-color-namer.src.color_namer import name_color

print(name_color("#ff5733"))  # → "Radiant Wasteland"
```

## Implementation Details

The algorithm:
1. Strips a leading `#` and validates that exactly six hexadecimal characters remain.
2. Converts the hex string to an integer.
3. Uses the integer to pick an adjective and a noun from two predefined lists via modulo arithmetic.
4. Returns the combined phrase.

Because the selection is based solely on the integer value, the same input always yields the same output.

## Testing

Run the tests with:

```bash
pytest utils/nightly-apocalypse-color-namer/tests
```

The test suite covers normal cases, edge cases, and error handling.
