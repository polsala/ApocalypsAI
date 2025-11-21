# Emoji Forecast

`emoji-forecast` is a lightweight Python utility that maps a calendar date to a whimsical weather emoji. The mapping is **deterministic** – the same date always yields the same emoji – and requires no external services.

## Features
- Zero runtime dependencies (standard library only).
- Deterministic output based on the date, making it safe for offline use and testing.
- Simple CLI for quick one‑liners:
  ```bash
  python -m emoji_forecast 2023-10-31
  # → 🌧️
  ```
- Easy to embed in CI pipelines, GitHub Actions, or chat‑bots.

## Usage
```python
from datetime import date
from src.forecast import get_forecast

print(get_forecast(date.today()))
```

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/nightly-emoji-forecast/utils/emoji-forecast/tests
```
