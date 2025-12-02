# Nightly Emoji Forecast

Utility that provides a deterministic, emoji‑based weather forecast for any date.

## Features
- Pure Python 3.11, no external dependencies.
- Deterministic output: the same date always yields the same three emojis.
- Small CLI (`python -m src.forecast`) prints today’s forecast.
- Easy to import and use in other scripts.

## Installation
```bash
# From the repository root
cd utils/nightly-emoji-forecast
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage
```bash
# As a module
python -m src.forecast

# As a library
>>> from src.forecast import get_emoji_forecast
>>> import datetime
>>> get_emoji_forecast(datetime.date(2023, 1, 1))
'🌤️☀️☀️'
```

## Testing
```bash
python -m unittest discover -s tests
```
