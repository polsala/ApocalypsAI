# Daily Zen Quote

A whimsical yet useful command‑line utility that prints a random Zen‑style quote. No network access required; quotes are bundled.

## Features

- Offline, deterministic (except randomness)
- Can be used as a CLI (`python -m daily_zen_quote`) or imported as a module.
- Includes a small library of curated Zen sayings.

## Installation

Copy the `utils/daily-zen-quote` folder into your project or install via pip (future).

## Usage

```bash
python -m daily_zen_quote
# or
python -c "from daily_zen_quote.src.zen_quote import get_random_quote; print(get_random_quote())"
```

## Testing

```bash
python -m unittest discover -s utils/daily-zen-quote/tests
```
