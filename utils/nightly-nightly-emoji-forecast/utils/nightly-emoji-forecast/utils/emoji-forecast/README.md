# Emoji Forecast

A tiny, self‑contained utility that turns any calendar date into a playful "weather" forecast expressed entirely in emojis. The algorithm is deterministic – the same date always yields the same forecast – making it perfect for scripts, CI messages, or just a daily smile.

## Usage

```bash
python -m emoji_forecast.src.forecast [YYYY-MM-DD]
```

If no date is supplied, the utility uses the current local date.

## API

```python
from emoji_forecast.src.forecast import get_emoji_forecast

forecast = get_emoji_forecast(date)  # date is a datetime.date instance
```

The function returns a string of emojis, e.g. `"☀️ 🌈"`.

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/nightly-emoji-forecast/utils/emoji-forecast/tests
```
