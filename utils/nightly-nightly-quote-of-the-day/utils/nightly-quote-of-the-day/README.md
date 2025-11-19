# Nightly Quote of the Day

`nightly-quote-of-the-day` is a self‑contained Python utility that prints a random inspirational quote from an internal list. It works completely offline and has no external dependencies beyond the Python standard library.

## Features
- No network access – quotes are bundled with the utility.
- Deterministic testing via a mockable random source.
- Simple CLI: `python -m src.quote_of_the_day` prints a quote to stdout.
- Easily extensible – add more quotes to `src/quote_of_the_day.py`.

## Installation & Usage
```bash
# From the repository root
python -m utils/nightly-quote-of-the-day/src/quote_of_the_day
```

## Development
Run the test suite with:
```bash
python -m pytest utils/nightly-quote-of-the-day/tests
```
