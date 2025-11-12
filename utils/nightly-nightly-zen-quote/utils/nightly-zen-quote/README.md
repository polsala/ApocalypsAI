# Nightly Zen Quote

`nightly-zen-quote` is a self‑contained Python utility that selects a Zen‑inspired quote at random.

## Features

- **Deterministic mode** – supply a `--seed` to get reproducible output (useful for tests or CI).
- **CLI** – run `python -m src.quote` to print a quote directly.
- **Zero external dependencies** – only the Python standard library.

## Usage

```bash
# Random quote (non‑deterministic)
python -m src.quote

# Deterministic quote – same seed always yields the same quote
python -m src.quote --seed 42
```

## Development

The source lives in `src/quote.py`. Tests are in `tests/test_quote.py` and can be run with:

```bash
python -m unittest discover -s tests
```
