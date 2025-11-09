# Random Compliment Generator

A whimsical yet useful utility that prints a random compliment to stdout.

## Features
- Zero external dependencies – pure Python 3.11.
- Deterministic unit tests using `unittest.mock`.
- Simple CLI (`python -m random_compliment_generator` or `python src/main.py`).

## Usage
```bash
# Run directly from the repository root
python utils/random-compliment-generator/src/main.py
```

You’ll see something like:
```
You have the coding prowess of a caffeinated squirrel!
```

## Extending
Add new compliments to `COMPLIMENTS` in `src/main.py` and they’ll be instantly available.

## Testing
```bash
python -m unittest utils/random-compliment-generator/tests/test_main.py
```
