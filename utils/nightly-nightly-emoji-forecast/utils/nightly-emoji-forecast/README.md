# Nightly Emoji Forecast

**What it does**

`nightly-emoji-forecast` provides a deterministic, whimsical "weather" forecast expressed as an emoji. The forecast is derived solely from the calendar date, so it works completely offline and produces the same result every time for a given day.

**Why it’s useful**

- Add a light‑hearted touch to CI logs, daily reports, or Slack messages.
- No external APIs or network calls – fully deterministic.
- Tiny footprint, pure Python 3.11, no dependencies.

**Installation**

```bash
# From the repository root
cd utils/nightly-emoji-forecast
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (empty, but kept for consistency)
```

**Usage**

```bash
# Print today’s emoji forecast
python -m src.forecast

# Or ask for a specific date (YYYY‑MM‑DD)
python -m src.forecast 2025-12-31
```

**API**

```python
from src.forecast import get_emoji_forecast

# Returns an emoji string for the supplied date (datetime.date) or today if None
emoji = get_emoji_forecast()
```

**Testing**

```bash
pytest -q
```
