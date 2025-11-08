# Random Compliment Generator

A whimsical yet useful command‑line tool that prints a random compliment.

## Features
- Zero external dependencies (uses only the Python standard library).
- Provides a small library function `get_compliment()` for programmatic use.
- Includes a deterministic test suite that mocks randomness.

## Installation
```bash
# From the repository root
cd utils/random-compliment-generator
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage
```bash
python -m src.compliment
```
Will output something like:
```
You have a brilliant mind!
```

## Library API
```python
from src.compliment import get_compliment

print(get_compliment())
```

## Testing
```bash
pytest -q
```
All tests run offline and are fully deterministic.
