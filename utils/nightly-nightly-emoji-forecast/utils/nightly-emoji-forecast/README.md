# Nightly Emoji Forecast

**What it does**

`nightly-emoji-forecast` generates a playful, deterministic "weather" forecast made entirely of emojis. The forecast is based on the current date (or any supplied date) and can be used as a daily terminal greeting, a Slack bot message, or just for a smile.

**Features**
- Zero external dependencies – pure Python 3.11.
- Deterministic output: the same date always yields the same forecast.
- Simple CLI: `python -m src.forecast` prints today’s forecast.
- Library mode: import `get_forecast` for programmatic use.

**Installation**
```bash
# From the repository root
cd utils/nightly-emoji-forecast
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (empty, kept for consistency)
```

**Usage**
```bash
# CLI – prints today’s forecast
python -m src.forecast

# CLI with custom date (YYYY‑MM‑DD)
python -m src.forecast 2023-10-31

# Library
>>> from src.forecast import get_forecast
>>> get_forecast()
'☀️ 🌤️ 🌈'
```

**Testing**
```bash
pytest -q
```
