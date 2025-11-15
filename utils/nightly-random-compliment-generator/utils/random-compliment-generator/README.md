# Random Compliment Generator

A whimsical utility that prints a random compliment to brighten your day. It can be used directly from the command line or imported as a Python module.

## Features
- Returns a random compliment from several friendly categories.
- Optional `--category` flag to focus on a theme (e.g., `coding`, `design`).
- Zero external dependencies – just the Python standard library.

## Installation & Usage
```bash
# Clone the repository (or copy the folder) and run:
python -m utils.random-compliment-generator.src.compliment

# With a specific category:
python -m utils.random-compliment-generator.src.compliment --category coding
```

## As a Library
```python
from compliment import get_compliment

print(get_compliment())               # any category
print(get_compliment('design'))       # specific category
```

## Testing
```bash
python -m unittest discover utils/random-compliment-generator/tests
```
