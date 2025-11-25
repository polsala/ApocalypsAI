# Nightly Zen Quote Generator

A whimsical yet useful utility that prints a random Zen‑style quote.

## Features
- Offline – all quotes are baked into the package.
- Optional `--max-length` filter to restrict quote length.
- Optional `--output <file>` to write the quote to a file instead of stdout.
- Zero external dependencies (pure Python 3.11).

## Installation
```bash
# From the repository root
python -m venv .venv && source .venv/bin/activate
pip install -e utils/nightly-zen-quote-generator
```

## Usage
```bash
python -m utils.nightly-zen-quote-generator.src.quote_generator
# With a length filter
python -m utils.nightly-zen-quote-generator.src.quote_generator --max-length 50
# Write to a file
python -m utils.nightly-zen-quote-generator.src.quote_generator --output quote.txt
```

## Testing
```bash
pytest utils/nightly-zen-quote-generator/tests
```
