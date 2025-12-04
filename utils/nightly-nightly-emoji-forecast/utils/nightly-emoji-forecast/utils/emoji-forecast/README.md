# Emoji Forecast

Generate a whimsical weather forecast expressed entirely in emojis for any given date. No external APIs; uses a deterministic algorithm based on the day of the year.

## Usage

```bash
python -m src.forecast 2023-12-25
# => 🎄❄️🥶
```

(Example output may vary.)

## API

```python
from src.forecast import get_emoji_forecast
forecast = get_emoji_forecast(date)  # date is a datetime.date
```
