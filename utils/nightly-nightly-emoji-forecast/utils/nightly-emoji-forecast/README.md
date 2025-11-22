# Nightly Emoji Forecast

`nightly-emoji-forecast` is a tiny, self‑contained utility that returns a deterministic *emoji forecast* for any given date. The forecast is purely deterministic – it hashes the day of the year into a short list of emojis – so it works offline and is perfect for adding a bit of levity to scripts, CI logs, or daily stand‑up notes.

## Usage
```bash
python -m nightly_emoji_forecast <YYYY-MM-DD>
```

Or, from Python:
```python
from nightly_emoji_forecast.src.forecast import get_emoji_forecast

print(get_emoji_forecast(date(2025, 11, 22)))  # ➜ "🌞"
```

## How it works
1. The day of the year (1‑366) is taken modulo the length of a curated emoji list.
2. The resulting index selects an emoji.
3. The same date always yields the same emoji, ensuring reproducibility.

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/nightly-emoji-forecast/tests
```
