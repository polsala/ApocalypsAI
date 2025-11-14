# Daily Zen Quote Generator

A whimsical utility that prints a Zen‑inspired quote of the day. The quote changes each day based on the current date, cycling through a built‑in list.

## Installation

You can run the script directly with Python 3.11 – no external dependencies required.

```bash
python -m utils.daily-zen-quote-generator.src.main
```

## Usage

```bash
python -m utils.daily-zen-quote-generator.src.main
```

The command prints a single quote to stdout.

## How it works

1. The script loads `quotes.json` (a static list of Zen‑style sayings).
2. It computes `index = today.toordinal() % len(quotes)`.
3. The quote at that index is printed.

Because the calculation is deterministic, the same date always yields the same quote.

## Testing

Run the bundled unit tests with:

```bash
python -m unittest discover -s utils/daily-zen-quote-generator/tests
```

The tests mock the current date to verify deterministic behavior.
