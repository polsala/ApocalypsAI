# Daily Zen Quote Dispenser

A tiny, self‑contained utility that serves a random Zen‑style quote each time you run it.  It can also filter quotes by tag (e.g., `mindfulness`, `humor`).

## Features

- **Zero dependencies** – pure Python 3.11 standard library.
- **CLI** – `python -m utils.daily-zen-quote-dispenser.src.zen` prints a quote.
- **Tag filtering** – `--tag <tag>` limits the pool.
- **Deterministic offline tests** – uses `unittest.mock` to control randomness.

## Usage

```bash
# Print any random Zen quote
python -m utils.daily-zen-quote-dispenser.src.zen

# Print a random quote tagged with "mindfulness"
python -m utils.daily-zen-quote-dispenser.src.zen --tag mindfulness
```

## Development

Run the test suite with:

```bash
python -m unittest discover -s utils/daily-zen-quote-dispenser/tests
```
