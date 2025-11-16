# Emoji Forecast

`emoji-forecast` provides a tiny, offline function that maps a calendar date to an emoji. The mapping is deterministic, reproducible, and requires no external data or network access.

## How it works

The algorithm counts the number of days since the Unix epoch (1970‑01‑01) and takes the remainder modulo a short list of emojis. The result is an emoji that can be used as a playful "forecast" for the day.

## Usage

```bash
python -m src.forecast            # prints today's emoji
python -m src.forecast 2025-01-01 # prints the emoji for a specific date
```

Or import the function in your own code:

```python
from src.forecast import get_emoji_for_date
from datetime import date

print(get_emoji_for_date(date.today()))
```

## Emoji list

```
☀️ 🌤️ ⛅ 🌥️ ☁️ 🌧️ ⛈️ 🌩️ 🌨️ ❄️ 🌪️ 🌈
```

## Testing

Run the test suite with:

```bash
python -m unittest discover -s tests
```
