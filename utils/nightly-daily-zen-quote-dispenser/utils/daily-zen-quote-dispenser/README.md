# Daily Zen Quote Dispenser

A whimsical yet practical utility that prints a random Zen‑style quote to the console. You can optionally filter quotes by a tag (e.g., `mindfulness`, `focus`).

## Features

- **Zero external dependencies** – pure Python 3.11.
- **Deterministic offline tests** – uses `unittest.mock` to control randomness.
- **CLI friendly** – `python -m daily_zen_quote_dispenser` prints a quote.

## Installation

Copy the folder `utils/daily-zen-quote-dispenser` into your project and run:

```bash
python -m utils.daily-zen-quote-dispenser.src.quote [--tag <tag>]
```

## Usage

```bash
# Print any random quote
python -m utils.daily-zen-quote-dispenser.src.quote

# Print a random quote tagged with "mindfulness"
python -m utils.daily-zen-quote-dispenser.src.quote --tag mindfulness
```

## Development

Run the test suite with:

```bash
python -m unittest discover -s utils/daily-zen-quote-dispenser/tests
```
