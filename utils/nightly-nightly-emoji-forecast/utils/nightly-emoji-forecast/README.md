# Nightly Emoji Forecast

**What it does**

`nightly-emoji-forecast` provides a tiny, self‑contained Python utility that returns a three‑emoji weather forecast for a supplied date (or for today if no date is given). The forecast is *deterministic*: the same date always yields the same emojis, making it safe for testing and offline use.

**Why it’s useful**

- Add a dash of personality to daily reports, CI logs, or commit messages.
- No external APIs – everything runs locally.
- Fully typed, zero‑dependency (standard library only).

**Installation**

```bash
# From the repository root
python -m venv .venv && source .venv/bin/activate
pip install -e utils/nightly-emoji-forecast
```

**Usage**

```python
from utils.nightly-emoji-forecast.src.forecast import get_forecast

# Specific date
print(get_forecast("2025-01-01"))  # e.g. 🌈🌧️🌤️

# Today (UTC)
print(get_forecast())
```

**Running the tests**

```bash
pytest utils/nightly-emoji-forecast/tests
```
