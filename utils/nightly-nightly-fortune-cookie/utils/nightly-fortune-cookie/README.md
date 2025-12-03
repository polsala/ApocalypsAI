# Nightly Fortune Cookie

`nightly-fortune-cookie` is a self‑contained Python utility that prints a random fortune‑cookie style message.

## Features
- No external dependencies (uses only the Python standard library).
- Deterministic unit tests via mocking.
- Simple CLI: `python -m src.fortune` prints a fortune.

## Usage
```bash
# Run the utility directly
python -m src.fortune

# Or import in your own code
from src.fortune import get_fortune
print(get_fortune())
```

## Adding New Fortunes
Edit the `FORTUNES` list in `src/fortune.py` and add your favorite sayings.
