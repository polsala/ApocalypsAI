# Random Compliment Generator

A whimsical yet useful command‑line tool that prints a random compliment.

## Features
- Zero external dependencies – pure Python 3.11.
- Deterministic unit tests using a mock for `random.choice`.
- Can be invoked directly via `python -m random_compliment` or imported as a library.

## Installation
```bash
# From the repository root
cd utils/random-compliment-generator
python -m venv .venv
source .venv/bin/activate
pip install .
```

## Usage
```bash
python -m random_compliment
# or
random-compliment
```

## Development
Run the test suite with:
```bash
pytest -q
```
