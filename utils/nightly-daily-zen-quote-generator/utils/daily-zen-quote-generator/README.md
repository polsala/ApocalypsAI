# Daily Zen Quote Generator

A whimsical yet practical utility that prints a random Zen‑style quote each time it runs.

## Features
- **Zero external dependencies** – all quotes are stored locally.
- **CLI interface** – `python -m daily_zen_quote_generator` prints a quote.
- **Category filtering** (optional) – choose `mindfulness`, `humor`, or `wisdom`.
- **Deterministic tests** – the random selection is mocked in the test suite.

## Usage
```bash
# Print any random quote
python -m daily_zen_quote_generator

# Print a quote from a specific category
python -m daily_zen_quote_generator --category mindfulness
```

## Development
Run the test suite with:
```bash
python -m unittest discover -s utils/daily-zen-quote-generator/tests
```
