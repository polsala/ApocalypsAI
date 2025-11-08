# Zen Quote Generator

A whimsical yet useful utility that prints a random Zen‑style quote to stdout.

## Features
- Zero external dependencies (uses only the Python standard library).
- Simple CLI (`python -m zenquote` or `python src/zenquote.py`).
- Deterministic unit tests using `unittest.mock`.

## Installation
Just copy the folder into your repository and run the module with Python 3.11 or later:
```bash
python -m zenquote
```
Or execute the script directly:
```bash
python utils/zen-quote-generator/src/zenquote.py
```

## Usage
```
$ python -m zenquote
The journey of a thousand miles begins with one step.
```

### Options
- `-n, --no-newline` – suppress the trailing newline (useful when piping).

## Testing
Run the bundled tests with:
```bash
python -m unittest discover utils/zen-quote-generator/tests
```
All tests are offline and deterministic.
