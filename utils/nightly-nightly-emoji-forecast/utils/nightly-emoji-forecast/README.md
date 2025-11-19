# Nightly Emoji Forecast

Utility that provides a deterministic emoji representing the weather forecast for a given date. No external APIs; uses a hash of the date to select from a fixed set of weather conditions.

## Usage

```bash
python -m src.forecast 2025-01-01
# ☀️
```

Run the tests with:

```bash
python -m unittest discover -s tests
```

## How it works

- Takes an ISO‑8601 date string (`YYYY‑MM‑DD`).
- Computes SHA‑256 hash of the string.
- Uses the hash to index into a list of weather conditions.
- Returns the corresponding emoji.
