# Nightly Emoji Forecast

Generate a whimsical, deterministic emoji weather forecast for any date.

## What it does
- No network calls – the forecast is derived from the date itself.
- Always returns the same three emojis for the same date, making it perfect for reproducible tests or daily fun messages.
- Provides a tiny CLI and a Python API.

## Usage

### CLI
```bash
python -m src.forecast 2023-10-31
# 🌧️☔️⛈️
```
If no date is supplied, it uses today’s date.

### Python API
```python
from src.forecast import get_forecast
import datetime

forecast = get_forecast(datetime.date(2023, 10, 31))
print(forecast)  # 🌧️☔️⛈️
```

## How it works
The utility converts the date to an integer seed (`YYYYMMDD`) and deterministically selects three emojis from a fixed list using simple modular arithmetic. This guarantees the same output for the same input without any randomness.

## Testing
Run the tests with:
```bash
python -m unittest discover -s tests
```
