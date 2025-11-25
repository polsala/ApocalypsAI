# Nightly Zen Quote Generator

**Utility name:** `nightly-zen-quote-generator`

## What it does

When executed, the tool selects a Zen‑style quote from an internal collection and prints it to stdout. It has no external dependencies and works completely offline.

## Why it’s useful

* Adds a touch of calm to noisy CI pipelines.
* Provides a quick source of inspiration for developers.
* Demonstrates a self‑contained Python utility with tests and documentation.

## Usage

```bash
python -m nightly_zen_quote_generator
```

Or, if you prefer the entry‑point script (once the utility is added to your `PATH`):

```bash
zen-quote
```

## Development

The source lives under `src/quote_generator.py`. Tests are in `tests/test_quote_generator.py` and use `unittest.mock` to keep them deterministic.
