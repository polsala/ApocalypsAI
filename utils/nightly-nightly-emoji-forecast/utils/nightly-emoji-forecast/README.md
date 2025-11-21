# Nightly Emoji Forecast

## Overview
`nightly-emoji-forecast` is a tiny, self‑contained Python utility that produces a playful *emoji weather* forecast for a supplied date (or today by default). The forecast is **deterministic** – the same date always yields the same emoji string – making it safe for offline testing and CI pipelines.

## Features
- Zero external dependencies (only the Python standard library).
- Deterministic output based on the date, so tests are reliable.
- Simple CLI: `python -m utils.nightly-emoji-forecast src/forecast.py [YYYY-MM-DD]`.
- Ready‑to‑use in GitHub Actions, README badges, Slack bots, etc.

## Usage
```bash
# Install nothing – just run with Python 3.11+
python -m utils.nightly-emoji-forecast src/forecast.py          # forecast for today
python -m utils.nightly-emoji-forecast src/forecast.py 2025-12-01  # forecast for a specific date
```

The script prints a short string of emojis, e.g.:
```
🌞 🌤️ 🌈
```

## Implementation Details
- The date is converted to an integer seed (`YYYYMMDD`).
- A `random.Random` instance seeded with that integer selects emojis from a curated list.
- The number of emojis (1‑3) is also derived from the same RNG, ensuring full reproducibility.

## Testing
The utility ships with a deterministic test suite that mocks the current date to verify output consistency. See `tests/test_forecast.py`.
