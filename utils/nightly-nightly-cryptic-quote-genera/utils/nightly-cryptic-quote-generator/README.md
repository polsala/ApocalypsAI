# Nightly Cryptic Quote Generator

A lightweight, self‑contained utility that prints a random cryptic quote each time it runs. You can optionally filter quotes by a tag (e.g., `wisdom`, `mystery`).

## Features
- Zero external dependencies – pure Python 3.11.
- Built‑in collection of 10+ quirky quotes.
- Simple CLI: `python -m utils.nightly-cryptic-quote-generator.src.quote_generator [--tag TAG]`
- Deterministic unit tests using `unittest.mock`.

## Usage
```bash
# Print any random quote
python -m utils.nightly-cryptic-quote-generator.src.quote_generator

# Print a random quote tagged as "wisdom"
python -m utils.nightly-cryptic-quote-generator.src.quote_generator --tag wisdom
```

## Structure
- `src/quote_generator.py` – core implementation and CLI entry point.
- `tests/test_quote_generator.py` – deterministic tests with mocks.
