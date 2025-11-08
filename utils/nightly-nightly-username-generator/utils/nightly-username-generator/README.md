# Nightly Username Generator

Generate a whimsical, pronounceable username from a numeric seed.

## Features
- Deterministic output – the same seed always yields the same username.
- No external dependencies; pure Python 3.11.
- Small and self‑contained – perfect for scripts, bots, or quick demos.

## Installation
```bash
# Clone the repository (or copy the folder) and install the utility's requirements.
# No third‑party packages are required.
```

## Usage
```bash
python -m utils.nightly-username-generator.src.generator --seed 42
# → "fluffy‑zebra"
```

You can also import the function in your own code:
```python
from utils.nightly-username-generator.src.generator import generate_username

print(generate_username(123))  # deterministic output
```

## How it works
The generator mixes three lists of syllables (prefix, middle, suffix) and selects an element from each list based on the provided seed using a simple linear congruential generator. The result is concatenated with a hyphen for readability.

## Testing
Run the bundled tests with:
```bash
python -m unittest discover utils/nightly-username-generator/tests
```
