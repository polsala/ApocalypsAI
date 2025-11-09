# Random Compliment Generator

A whimsical utility that prints a random compliment to brighten your day. It can be used as a command‑line tool or imported as a module. Provide an optional integer seed for deterministic output, which is handy for testing or reproducible scripts.

## Installation

Copy the `src/compliment.py` file into your project or run the utility directly from this repository.

## Usage

```bash
python -m utils.random-compliment-generator.src.compliment   # prints a random compliment
python -m utils.random-compliment-generator.src.compliment --seed 42   # deterministic
```

Or as a library:

```python
from utils.random-compliment-generator.src.compliment import get_compliment

print(get_compliment())          # random
print(get_compliment(seed=42))   # deterministic
```

## Testing

Run the tests with:

```bash
python -m unittest discover utils/random-compliment-generator/tests
```
