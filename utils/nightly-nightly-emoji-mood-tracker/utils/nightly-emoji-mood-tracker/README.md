# Nightly Emoji Mood Tracker

A whimsical yet practical utility for tracking your daily mood using emojis.

## Features
- Log a mood for the current day (`emoji-mood log 😄`).
- Show a summary of the last N days (`emoji-mood summary 7`).
- Data is stored locally in a JSON file (`~/.emoji_mood_tracker.json`).
- Fully offline, no external APIs.

## Installation
```bash
# From the repository root
python -m venv .venv
source .venv/bin/activate
pip install -r utils/nightly-emoji-mood-tracker/requirements.txt  # (empty, just for future use)
```

## Usage
```bash
python -m utils.nightly-emoji-mood-tracker.src.mood_tracker log 😄
python -m utils.nightly-emoji-mood-tracker.src.mood_tracker summary 7
```

## Testing
```bash
pytest utils/nightly-emoji-mood-tracker/tests
```
