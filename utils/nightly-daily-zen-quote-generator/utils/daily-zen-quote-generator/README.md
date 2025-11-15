# Daily Zen Quote Generator

A lightweight, self‑contained utility that prints a random Zen‑style quote to the console.

## Features
- No external network access – quotes are bundled in the package.
- Pure Python 3.11, no third‑party dependencies.
- Deterministic unit tests using mocks.

## Usage
```bash
python -m daily_zen_quote_generator
```
Will output a random quote, e.g.:
```
The journey of a thousand miles begins with one step.
```

## Development
Run the test suite with:
```bash
python -m unittest discover -s utils/daily-zen-quote-generator/tests
```
