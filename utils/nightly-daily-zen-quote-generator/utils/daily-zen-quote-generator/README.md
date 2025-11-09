# Daily Zen Quote Generator

A whimsical yet practical utility that prints a random Zen‑style quote each time you run it. The quotes are bundled with the package, so the tool works completely offline.

## Features
- Zero external dependencies (pure Python 3.11).
- Bundled collection of thoughtful quotes.
- Simple CLI: `python -m daily_zen_quote_generator`.
- Deterministic unit tests using mocks.

## Usage
```bash
# From the repository root
python -m utils.daily-zen-quote-generator.src.quote_generator
```

You’ll see something like:
```
"The journey of a thousand miles begins with one step." – Lao Tzu
```

## Development
Run the test suite with:
```bash
python -m unittest discover utils/daily-zen-quote-generator/tests
```
