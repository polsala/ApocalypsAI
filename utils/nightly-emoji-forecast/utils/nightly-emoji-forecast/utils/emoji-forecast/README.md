# Emoji Forecast

Generate a whimsical weather forecast represented by emojis for any given date.

## Usage

```bash
python -m emoji_forecast 2023-10-31
# Output: 🌧️☀️🌈
```

Or import the function in your own code:

```python
from emoji_forecast import get_forecast
import datetime
print(get_forecast(datetime.date(2023, 10, 31)))
```

## How it works

The forecast is **deterministic** – the same date always yields the same three‑emoji sequence. It is derived from the date’s ordinal value, ensuring no external randomness or network calls.
