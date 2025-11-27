# Nightly Emoji Forecast

A tiny, self‑contained utility that prints a whimsical weather forecast using emojis.

## How it works

* The forecast is **deterministic** – it is derived from the date's ordinal value, so the same date always yields the same emoji.
* No external APIs are called; everything runs offline.
* Implemented in pure Python 3.11 with only the standard library.

## Usage

```bash
# Forecast for today (default)
python -m src.forecast

# Forecast for a specific date (YYYY‑MM‑DD)
python -m src.forecast 2024-12-31
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s tests
```
