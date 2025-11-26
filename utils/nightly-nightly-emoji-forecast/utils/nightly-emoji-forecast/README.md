# Nightly Emoji Forecast

Generate a whimsical emoji weather forecast for any date. The forecast is **deterministic** – the same date always yields the same emojis – and requires no external APIs.

## Usage

```bash
# As a module (defaults to today)
python -m src.forecast

# For a specific date (YYYY-MM-DD)
python -m src.forecast 2025-12-31
```

Or import the helper in your own Python code:

```python
from src.forecast import generate_forecast
import datetime

print(generate_forecast(datetime.date(2025, 12, 31)))
```

## How it works

* The utility maps a small set of weather‑related emojis.
* It seeds Python's `random.Random` with the date's ordinal (`date.toordinal()`).
* Three emojis are chosen deterministically from the list.
* Because the algorithm is pure‑Python, it works offline and is fully testable.

## License

MIT – see the repository's top‑level `LICENSE` file.
