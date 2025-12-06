# Haiku of the Day

A whimsical utility that prints a deterministic haiku based on the current date. No network access, no external data – everything is generated locally.

## Features
- Generates a classic 5‑7‑5 haiku.
- Deterministic: the same date always yields the same poem.
- Pure Python 3.11, no third‑party dependencies.

## Usage
```bash
# Run directly
python -m src.haiku

# Or import in your own code
from src.haiku import generate_haiku
print(generate_haiku())
```

## Testing
```bash
python -m unittest discover -s tests
```
