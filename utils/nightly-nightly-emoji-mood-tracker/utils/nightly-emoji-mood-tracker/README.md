# Emoji Mood Tracker

A whimsical yet practical command‑line tool that lets you record your daily mood with an emoji and view a quick summary of recent moods.

## Features
- Log a mood for any date using a single emoji.
- Store data locally in a JSON file (`~/.emoji_mood_tracker.json`).
- Show a plain‑text summary for the last *N* days.
- Zero external dependencies – pure Python 3.11.

## Installation
Just copy the utility into your project and run it with Python:
```bash
python -m src.mood_tracker <command> [args]
```

## Usage
```bash
# Add a mood entry
python -m src.mood_tracker add 2023-10-01 😊

# Show a summary for the last 7 days
python -m src.mood_tracker summary 7
```

The data file is created automatically on first use. Feel free to edit it manually if you like.

## License
MIT – see the repository LICENSE file.
