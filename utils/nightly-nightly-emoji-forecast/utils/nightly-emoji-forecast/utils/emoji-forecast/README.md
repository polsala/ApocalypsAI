# Emoji Forecast Utility

A tiny, self‑contained Python utility that produces a whimsical, deterministic emoji "weather" forecast for any given date.

## Features
- No external dependencies beyond the Python standard library.
- Deterministic output: the same date always yields the same emoji.
- Simple CLI (`python -m src.forecast`) prints today’s forecast.
- Fully unit‑tested with offline mocks.

## Usage
```bash
# Run the CLI (prints today’s forecast)
python -m src.forecast

# Use as a library
>>> import datetime
>>> from src.forecast import get_forecast
>>> get_forecast(datetime.date(2023, 1, 1))
"🌦️"
```
