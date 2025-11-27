# Nightly Emoji Mood Tracker

A whimsical yet practical command‑line tool that lets you record your daily mood with a single emoji and later view a concise summary.

## Features
- **Log a mood** for any date (defaults to today) using an emoji string.
- **Persist data** in a tiny JSON file under `~/.emoji_mood.json` – no external services required.
- **Show a summary** of how many times each emoji was used.

## Installation
```bash
# From the repository root
python -m venv .venv
source .venv/bin/activate
pip install -e utils/nightly-emoji-mood-tracker
```

## Usage
```bash
# Log today's mood (e.g., happy face)
python -m utils.nightly-emoji-mood-tracker src.mood_tracker log 😊

# Log a mood for a specific date (YYYY‑MM‑DD)
python -m utils.nightly-emoji-mood-tracker src.mood_tracker log 2024-10-31 😢

# Show summary
python -m utils.nightly-emoji-mood-tracker src.mood_tracker summary
```

## Testing
```bash
pytest utils/nightly-emoji-mood-tracker/tests
```

---
*Created by the ApocalypsAI Nightly Integrator.*
