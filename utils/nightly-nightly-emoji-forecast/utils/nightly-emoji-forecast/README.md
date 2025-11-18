# Nightly Emoji Forecast

`nightly-emoji-forecast` is a tiny, self‑contained Python utility that returns a single emoji representing the current weather for a given city.

## Features
- Maps common weather conditions to clear, expressive emojis.
- Offline‑friendly: the core logic is pure Python; the external weather fetch is deliberately left as a stub so it can be mocked in tests.
- Simple CLI: `python -m utils.nightly_emoji_forecast.src.forecast <city>` prints `<city>: <emoji>`.

## Installation & Usage
```bash
# From the repository root
python -m utils.nightly_emoji_forecast.src.forecast "San Francisco"
```

If you integrate a real weather API, replace the `_fetch_weather` stub in `forecast.py` with your implementation.

## Testing
```bash
python -m unittest discover utils/nightly-emoji-forecast/tests
```
All tests run offline using `unittest.mock`.
