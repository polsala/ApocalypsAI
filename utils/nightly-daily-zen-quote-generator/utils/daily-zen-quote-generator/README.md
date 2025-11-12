# Daily Zen Quote Generator

A whimsical yet useful utility that prints a random Zen‑inspired quote to the console. No network required; quotes are bundled.

## Usage

```bash
python -m daily_zen_quote_generator
```

Optional arguments:

- `--count N` : print N random quotes (default 1).

## How it works

Selects a quote from a hard‑coded list using `random.choice`. The utility is self‑contained and includes deterministic tests that mock the random selection.
