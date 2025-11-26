# Emoji Forecast

A tiny utility that generates a whimsical emoji "weather forecast" for any given date. The forecast is **deterministic** – the same date always yields the same sequence of emojis – making it safe for offline use and reproducible tests.

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
pip install .
```

(Or simply run the script directly; it has no external dependencies.)

## Usage

```bash
# Today's forecast
python -m utils.nightly-emoji-forecast.src.forecast

# Forecast for a specific date (YYYY‑MM‑DD)
python -m utils.nightly-emoji-forecast.src.forecast --date 2025-12-01
```

Typical output looks like:

```
🌞 🌦️ 🌈
```

## How it works

1. The supplied date (or today) is converted to an integer seed in the form `YYYYMMDD`.
2. A `random.Random` instance seeded with this value selects **three** emojis from a curated list.
3. The emojis are joined with spaces and printed.

Because the seed is derived solely from the date, the result is repeatable and requires no network access.

## Testing

Run the test suite with:

```bash
python -m unittest discover utils/nightly-emoji-forecast/tests
```

The tests mock the emoji list and the date to guarantee deterministic behaviour.
