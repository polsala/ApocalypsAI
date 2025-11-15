# Random Compliment Generator

A whimsical yet useful utility that prints a random compliment to the console. You can optionally specify a category (e.g., `work`, `friendship`, `self`) to get a themed compliment.

## Features

- **Zero dependencies** – pure Python 3.11 standard library.
- **Deterministic tests** – uses `unittest.mock` to stub randomness.
- **CLI usage** – `python -m random_compliment [--category <cat>]`.

## Installation

Copy the `utils/random-compliment-generator` folder into your project and run the module directly:

```bash
python -m utils.random-compliment-generator.src.compliment
```

## Usage

```bash
# Any compliment
python -m utils.random-compliment-generator.src.compliment

# Category‑specific compliment
python -m utils.random-compliment-generator.src.compliment --category work
```

## Development

Run the test suite with:

```bash
python -m unittest discover -s utils/random-compliment-generator/tests
```
