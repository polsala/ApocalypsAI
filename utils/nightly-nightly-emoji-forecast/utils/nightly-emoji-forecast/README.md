# Nightly Emoji Forecast

A tiny, self‑contained utility that produces a deterministic, whimsical "weather forecast" made entirely of emojis. No network calls, no external APIs – the forecast is derived from a SHA‑256 hash of the supplied date, ensuring the same input always yields the same output.

## Features
- Pure Python 3.11, no third‑party dependencies.
- CLI interface: `python -m src.forecast [DATE] [-n NUM]`
- Adjustable number of forecast emojis (default 3).
- Fully documented and unit‑tested.

## Usage
```bash
# Forecast for today (default)
python -m src.forecast

# Forecast for a specific date
python -m src.forecast 2025-12-31

# Forecast with a custom length
python -m src.forecast 2025-12-31 -n 5
```

## How it works
1. The date string (ISO format) is hashed with SHA‑256.
2. The integer representation of the hash is used to index into a fixed list of weather‑related emojis.
3. The first `n` emojis (wrapping around the list) form the forecast.

## License
MIT – see the root `LICENSE` file.
