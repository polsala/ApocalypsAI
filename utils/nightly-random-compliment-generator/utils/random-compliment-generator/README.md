# Random Compliment Generator

A whimsical yet useful command‑line utility that prints a random compliment. Perfect for sprinkling positivity in scripts, CI logs, or just for fun.

## Features
- Zero external dependencies (uses only Python's standard library).
- Provides a `get_random_compliment()` function for programmatic use.
- Includes a CLI entry point: `python -m random_compliment_generator`.
- Fully tested with deterministic offline tests using mocks.

## Installation
Simply copy the `utils/random-compliment-generator` folder into your project and run the script with Python 3.11+.

```bash
python -m utils.random-compliment-generator.src.compliment
```

## Usage
```python
from utils.random-compliment-generator.src.compliment import get_random_compliment

print(get_random_compliment())
```

## Testing
Run the tests with:
```bash
python -m unittest discover utils/random-compliment-generator/tests
```
