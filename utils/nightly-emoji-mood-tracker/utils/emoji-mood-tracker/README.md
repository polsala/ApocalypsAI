# Emoji Mood Tracker

A whimsical yet practical command‑line tool that lets you record your daily mood with an emoji and view a quick summary of how many times each mood was logged.

## Features
- **Add today's mood** with a single emoji.
- **Show today's mood**.
- **Summary** of all recorded moods.
- Stores data in a local `mood_log.json` file (human‑readable).

## Installation
```bash
# From the repository root
cd utils/emoji-mood-tracker
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (no external deps needed)
```

## Usage
```bash
# Record a mood (e.g., 😊)
python -m src.tracker add 😊

# Show today's mood
python -m src.tracker show

# Show a summary of all moods
python -m src.tracker summary
```

## Testing
```bash
python -m unittest discover -s tests
```
