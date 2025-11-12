# Random Compliment Generator

A whimsical yet useful command‑line utility that serves up a random compliment.

## Features

- Choose a category (`general`, `work`, `coding`) or let the tool pick any.
- Zero external dependencies – pure Python 3.11.
- Fully tested with deterministic, offline unit tests.

## Installation

Copy the `src/compliment.py` file into your project or add the whole folder to your `PYTHONPATH`.

```bash
# Example: run directly from the utils folder
python -m utils.random-compliment-generator.src.compliment
```

## Usage

```bash
# Random compliment from any category
python -m utils.random-compliment-generator.src.compliment

# Specify a category
python -m utils.random-compliment-generator.src.compliment --category coding
```

## Development

Run the test suite with:

```bash
python -m unittest discover -s utils/random-compliment-generator/tests
```
