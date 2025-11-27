# Nightly Emoji Forecast

**What it does**

`nightly-emoji-forecast` provides a tiny, self‑contained Python utility that returns a weather forecast for a given date (or today) expressed purely with emojis. The forecast is *deterministic* – it is derived from a SHA‑256 hash of the ISO‑formatted date, so the same date always yields the same result. No network calls, no external data sources.

**Why it’s useful**

- Perfect for adding a splash of fun to daily scripts, CI logs, or chat bots.
- Completely offline – ideal for environments with restricted networking.
- Deterministic output makes testing trivial.

**Installation**

```bash
# From the repository root
cd utils/nightly-emoji-forecast
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (no extra deps needed)
```

**Usage**

```bash
# As a module
python -m src.forecast          # prints today’s forecast

# Or import in your own code
from src.forecast import get_forecast
print(get_forecast())            # today
print(get_forecast(date=datetime.date(2023, 1, 1)))
```

**Testing**

```bash
pytest -q
```

---

*Created by the ApocalypsAI Nightly Integrator.*
