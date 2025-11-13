# Daily Zen Quote Dispenser

A whimsical yet useful utility that prints a random Zen‑style quote to the console.

## Features
- Built‑in collection of short, inspirational quotes.
- Optional `--theme` flag to limit quotes to a specific topic (e.g., *mindfulness*, *growth*).
- Optional `--seed` flag for deterministic output – handy for testing or reproducible scripts.
- Zero third‑party dependencies; pure Python 3.11.

## Installation
Simply copy the `utils/daily-zen-quote-dispenser` folder into your project and run the script:
```bash
python -m utils.daily-zen-quote-dispenser.src.quote
```

## Usage
```bash
# Random quote
python -m utils.daily-zen-quote-dispenser.src.quote

# Quote from a specific theme
python -m utils.daily-zen-quote-dispenser.src.quote --theme mindfulness

# Deterministic quote (same seed always yields same result)
python -m utils.daily-zen-quote-dispenser.src.quote --seed 42
```

## Development
Run the test suite with:
```bash
python -m unittest discover utils/daily-zen-quote-dispenser/tests
```
