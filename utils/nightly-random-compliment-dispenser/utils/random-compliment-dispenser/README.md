# Random Compliment Dispenser

Utility that returns a random, friendly compliment for a given name. Great for chat‑bots, CLI tools, or just brightening someone's day.

## Features
- Zero external dependencies – pure Python 3.11.
- Deterministic unit tests using `unittest.mock`.
- Simple API: `get_compliment(name: str) -> str`.

## Installation
Copy the `src/compliment.py` file into your project or add this utility as a submodule.

## Usage
```python
from src.compliment import get_compliment

print(get_compliment("Alice"))
# → "You're a shining star, Alice!" (randomly chosen)
```

## Running the tests
```bash
python -m unittest discover -s utils/random-compliment-dispenser/tests
```
