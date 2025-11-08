# Random Compliment Generator

A whimsical yet useful utility that prints a random compliment to stdout.

## Features
- Zero external dependencies – pure Python 3.11.
- Simple CLI: `python -m random_compliment_generator`
- Deterministic unit tests using a mock for `random.choice`.

## Usage
```bash
$ python -m random_compliment_generator
You are a brilliant problem‑solver!
```

## Installation
The utility is self‑contained; just copy the `utils/random-compliment-generator` folder into your project and run the module.

## Testing
```bash
cd utils/random-compliment-generator
python -m unittest discover -v
```
