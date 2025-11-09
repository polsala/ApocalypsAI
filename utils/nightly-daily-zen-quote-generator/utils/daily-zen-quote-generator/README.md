# Daily Zen Quote Generator

A lightweight utility that prints a random Zen‑style quote.

## Features

- **Deterministic mode** – pass `--seed <int>` to get a reproducible quote.
- **Zero external dependencies** – pure Python 3.11 standard library.
- **Self‑contained** – quotes are bundled in `quotes.json`.

## Usage

```bash
python -m utils.daily-zen-quote-generator.src.zen_quote [--seed 42]
```

If `--seed` is omitted a truly random quote is chosen.

## Testing

Run the test suite with:

```bash
python -m unittest discover utils/daily-zen-quote-generator/tests
```
