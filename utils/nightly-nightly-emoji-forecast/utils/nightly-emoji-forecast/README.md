# Nightly Emoji Forecast

`nightly-emoji-forecast` is a tiny, self‑contained Python utility that returns a deterministic, emoji‑styled weather forecast for a supplied date (or today by default).

## Features
- **Deterministic** – the same date always yields the same emoji, no external APIs.
- **Zero dependencies** – only the Python standard library.
- **CLI friendly** – run `python -m src.forecast` or import the `get_forecast` function.

## Usage
```bash
# As a module (defaults to today)
python -m src.forecast

# Specify a date (YYYY‑MM‑DD)
python -m src.forecast 2023-10-31
```

Output example:
```
Today's forecast: 🌧️
```

## How it works
The utility maps the day‑of‑year to one of nine weather emojis:
```
0: ☀️  (Sunny)
1: 🌤️ (Partly Cloudy)
2: 🌧️ (Rainy)
3: ⛈️ (Stormy)
4: 🌨️ (Snowy)
5: 🌈 (Rainbow)
6: 🌪️ (Tornado)
7: 🌫️ (Foggy)
8: 🌙 (Clear Night)
```
The mapping is deterministic: `index = (day_of_year - 1) % 9`.

## Testing
Run the bundled pytest suite:
```bash
pytest -q
```
All tests are offline and deterministic.
