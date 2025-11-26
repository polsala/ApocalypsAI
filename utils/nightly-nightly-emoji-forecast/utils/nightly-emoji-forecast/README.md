# Nightly Emoji Forecast

**Utility name:** `nightly-emoji-forecast`

## What it does

`nightly-emoji-forecast` produces a single emoji that represents a “weather forecast” for a given day. The result is **deterministic** – the same date always yields the same emoji – making it safe for offline testing and CI pipelines.

## How to use

```bash
python -m src.forecast          # prints today’s emoji forecast
python -m src.forecast 2023-01-01  # prints the forecast for a specific date
```

You can also import the helper function in your own Python code:

```python
from src.forecast import get_daily_emoji_forecast

print(get_daily_emoji_forecast())               # today
print(get_daily_emoji_forecast(date=date(2023, 1, 1)))
```

## Design notes

* The forecast is derived from a SHA‑256 hash of the ISO‑formatted date, ensuring a uniform distribution across a fixed list of emojis.
* No external network calls – fully offline.
* Includes a tiny test suite that uses mocks to guarantee deterministic behavior.

## License

MIT – see the root `LICENSE` file.
