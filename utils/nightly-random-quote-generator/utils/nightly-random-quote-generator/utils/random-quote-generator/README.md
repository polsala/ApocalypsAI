# Random Quote Generator

A lightweight, self‑contained utility that prints a random whimsical quote.

## Features

- Built‑in collection of quotes with optional categories (e.g., *inspiration*, *humor*).
- CLI interface:
  ```bash
  python -m random_quote_generator [--category <cat>]
  ```
- No external dependencies – pure Python 3.11.
- Fully tested with deterministic mocks.

## Usage

```bash
# Print any random quote
python -m random_quote_generator

# Print a random quote from the "humor" category
python -m random_quote_generator --category humor
```

## Development

Run the test suite with:
```bash
python -m unittest discover -s utils/nightly-random-quote-generator/utils/random-quote-generator/tests
```
