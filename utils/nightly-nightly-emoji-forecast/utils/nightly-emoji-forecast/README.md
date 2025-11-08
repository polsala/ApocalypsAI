# Nightly Emoji Forecast

Generate a playful emoji‑based weather forecast for any date without reaching out to external services.

## How it works

* The utility hashes the ISO‑formatted date (`YYYY‑MM‑DD`) with SHA‑256.
* The resulting integer is taken modulo the number of available emojis (12).
* The selected emoji is returned as the forecast.

Because the algorithm is pure and deterministic, the same date always yields the same emoji, making the utility safe for offline CI runs.

## Usage

```bash
# Run as a module
python -m forecast 2025-12-25
# Output (example): 🌨️
```

You can also import the library in your own Python code:

```python
from src.forecast import get_emoji_forecast
import datetime

today = datetime.date.today()
print(get_emoji_forecast(today))
```

## Development

* **Language**: Python 3.11
* **Dependencies**: only the Python standard library
* **Tests**: run `python -m unittest discover -s tests` from the utility root.
