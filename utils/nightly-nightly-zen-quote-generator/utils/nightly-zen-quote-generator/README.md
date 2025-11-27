# Nightly Zen Quote Generator

A tiny, self‑contained utility that prints a short zen‑style quote.  It can operate completely offline and, when given a numeric seed, will always return the same quote – perfect for reproducible tests or daily “quote of the day” scripts.

## Features

- No external network calls – all quotes are baked into the source.
- Deterministic output when a seed is supplied.
- Simple CLI (`python -m src.quote_generator [--seed <int>]`).
- Comes with a full test suite that uses mocks to stay offline.

## Usage

```bash
# Random quote (non‑deterministic)
python -m src.quote_generator

# Deterministic quote with a seed
python -m src.quote_generator --seed 42
```

## Development

The utility lives in `src/quote_generator.py`.  Tests are in `tests/test_quote_generator.py` and can be run with:

```bash
python -m unittest discover -s tests
```
