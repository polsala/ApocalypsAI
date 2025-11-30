# Emoji Forecast Utility

`emoji-forecast` is a tiny, self‑contained Python utility that turns a date range into a whimsical weather forecast expressed entirely in emojis.

## Features
- **Deterministic** – the same start/end dates always produce the same emoji sequence (no network calls).
- **Zero dependencies** – only the Python standard library.
- **CLI & library** – use it from the command line or import `generate_forecast` in your own code.

## Installation
```bash
# From the repository root
cd utils/nightly-emoji-forecast/utils/emoji-forecast
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (empty, kept for future proofing)
```

## Usage
```bash
python -m src.forecast 2023-04-01 2023-04-07
```
Will output something like:
```
2023-04-01: ☀️
2023-04-02: 🌧️
2023-04-03: ⛅
...```

Or as a library:
```python
from utils.emoji_forecast.src.forecast import generate_forecast
forecast = generate_forecast("2023-04-01", "2023-04-07")
print(forecast)  # ['☀️', '🌧️', '⛅', ...]
```

## Testing
```bash
python -m unittest discover -s tests
```
All tests run offline and are fully deterministic.
