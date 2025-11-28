# Nightly Emoji Forecast

**What it does**

`nightly-emoji-forecast` generates a playful, deterministic "weather" forecast expressed entirely in emojis. The forecast is derived from the current date, so it changes daily but is reproducible for any given date without any network calls.

**Why it’s useful**

- Adds a bit of fun to daily stand‑ups or CI logs.
- No external dependencies – works offline.
- Deterministic output makes testing trivial.

**Installation**

```bash
# From the repository root
cd utils/nightly-emoji-forecast
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (empty for now)
```

**Usage**

```bash
python -m src.forecast          # prints today’s forecast
python -m src.forecast 2025-12-25  # prints forecast for a specific date
```

**Running the tests**

```bash
pytest -q
```
