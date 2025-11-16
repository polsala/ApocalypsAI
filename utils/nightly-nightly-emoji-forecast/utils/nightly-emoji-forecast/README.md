# Nightly Emoji Forecast

A tiny utility that generates a whimsical emoji weather forecast for any given date. Perfect for adding a splash of fun to daily reports, README badges, or Slack messages.

## Features

- **Deterministic**: the same date always yields the same forecast.
- **No external dependencies** – pure Python 3.11.
- **CLI**: `python -m utils.nightly-emoji-forecast.src.emoji_forecast [YYYY-MM-DD]`
- **Programmatic API**: `get_forecast(date)`.

## Example

```bash
$ python -m utils.nightly-emoji-forecast.src.emoji_forecast 2025-11-16
🌤️ 🌦️ 🌈
```

## Usage

```python
import datetime
from utils.nightly_emoji_forecast.src.emoji_forecast import get_forecast, format_forecast

date = datetime.date.today()
emojis = get_forecast(date)
print(format_forecast(emojis))
```

## License

MIT
