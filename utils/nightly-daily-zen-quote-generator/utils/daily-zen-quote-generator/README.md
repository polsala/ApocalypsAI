# Daily Zen Quote Generator

A tiny utility that prints a random Zen‑inspired quote.  It works completely offline – the quotes are baked into the package – and it offers an optional `--max‑length` flag to limit the length of the output.

## Features
- No network access – all quotes are stored locally.
- Simple CLI (`python -m src.quote_generator`).
- Deterministic unit tests using `unittest.mock`.

## Usage
```bash
# Print any random quote
python -m src.quote_generator

# Print a quote no longer than 60 characters
python -m src.quote_generator --max-length 60
```

## Development
Run the test suite with:
```bash
python -m unittest discover -s utils/daily-zen-quote-generator/tests
```
