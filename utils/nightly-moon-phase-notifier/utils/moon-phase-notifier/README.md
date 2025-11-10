# Moon Phase Notifier

A lightweight, self‑contained utility that tells you the moon phase for a given date.

## Features
- Pure Python 3.11, no external dependencies.
- Simple CLI: `python -m moon_phase [--date YYYY-MM-DD]`
- Returns a human‑readable phase name and an emoji (🌑, 🌒, 🌓, 🌔, 🌕, 🌖, 🌗, 🌘).
- Deterministic unit tests covering known lunar dates.

## Installation
```bash
# From the repository root
cd utils/moon-phase-notifier
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage
```bash
# Today
python -m src.moon_phase

# Specific date
python -m src.moon_phase --date 2023-02-05
```

## Testing
```bash
pytest -q
```
