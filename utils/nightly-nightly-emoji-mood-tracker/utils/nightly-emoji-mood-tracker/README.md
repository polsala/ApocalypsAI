# Nightly Emoji Mood Tracker

A whimsical yet practical command‑line tool that lets you record your daily mood with an emoji and later view a simple summary of how often each mood was logged.

## Features
- **Add a mood entry** for a specific date (defaults to today).
- **Show a summary** of counts per emoji.
- Stores data in a tiny JSON file in the user's home directory (`~/.emoji_mood.json`).
- Zero external dependencies – pure Python 3.11 standard library.

## Installation
```bash
# From the repository root
python -m venv .venv && source .venv/bin/activate
pip install -e utils/nightly-emoji-mood-tracker
```

## Usage
```bash
# Add today's mood (e.g., happy face)
python -m utils.nightly-emoji-mood-tracker.src.mood_tracker add 😊

# Add a mood for a specific date (YYYY‑MM‑DD)
python -m utils.nightly-emoji-mood-tracker.src.mood_tracker add 2025-11-01 😢

# Show summary
python -m utils.nightly-emoji-mood-tracker.src.mood_tracker summary
```

## Development & Testing
Run the bundled tests with:
```bash
python -m unittest discover utils/nightly-emoji-mood-tracker/tests
```

The tests use `unittest.mock` to avoid touching the real filesystem.
