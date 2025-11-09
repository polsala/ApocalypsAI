# Random Compliment Generator

A whimsical yet useful command‑line tool that prints a random compliment each time it runs.

## Features
- Zero external dependencies (uses only Python's standard library).
- Provides a Python API (`get_random_compliment`) for programmatic use.
- Includes a tiny CLI (`python -m random_compliment`) for quick terminal fun.
- Fully tested with deterministic, offline unit tests.

## Installation
Simply copy the `utils/random-compliment-generator` folder into your project and run:
```bash
python -m utils.random-compliment-generator.src.compliment
```

Or import the function in your own code:
```python
from utils.random-compliment-generator.src.compliment import get_random_compliment
print(get_random_compliment())
```

## License
MIT – feel free to spread the compliments! 🎉
