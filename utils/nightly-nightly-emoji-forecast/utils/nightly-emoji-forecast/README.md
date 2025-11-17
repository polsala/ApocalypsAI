# Nightly Emoji Forecast

A tiny, self‑contained utility that prints a single emoji representing the "forecast" for today. The forecast is deterministic – it is derived from the current date, so the same day always yields the same emoji.

## Why?
- Add a splash of personality to daily logs or CI output.
- Perfect for Slack/Discord bots that want a quick mood indicator.
- No external APIs; works completely offline.

## Usage
```bash
python -m utils.nightly-emoji-forecast.src.forecast
```
Or import the function in your own code:
```python
from utils.nightly-emoji-forecast.src.forecast import get_emoji_forecast
print(get_emoji_forecast())
```

## Implementation Details
- The forecast is chosen from a curated list of emojis.
- A `random.Random` instance is seeded with the ISO‑format date string (`YYYY‑MM‑DD`).
- This guarantees the same emoji for a given calendar day across runs and machines.

## Testing
Run the bundled tests with:
```bash
python -m unittest discover utils/nightly-emoji-forecast/tests
```
