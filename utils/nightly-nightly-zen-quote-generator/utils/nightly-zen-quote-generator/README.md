# Nightly Zen Quote Generator

A whimsical yet practical utility that prints a random zen‑style quote. Perfect for:

- Adding a daily dose of inspiration to your terminal startup.
- Embedding in CI logs for a touch of calm.
- Any script that needs a lightweight, offline quote source.

## Features

- **Zero external dependencies** – just the Python standard library.
- Deterministic output when a seed is supplied (useful for testing).
- Simple CLI: `python -m quote_generator [--seed <int>]`.

## Usage

```bash
# Random quote each run
python -m quote_generator

# Deterministic quote (useful for scripts or tests)
python -m quote_generator --seed 42
```

## Development

The utility lives in `src/quote_generator.py`. Tests are in `tests/test_quote_generator.py` and can be run with:

```bash
python -m unittest discover -s utils/nightly-zen-quote-generator/tests
```
