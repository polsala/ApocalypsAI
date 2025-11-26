# Emoji Mood Tracker

A whimsical yet practical utility that lets you record your daily mood with a single emoji and later view a quick summary.

## Features
- **Add mood** for any date (defaults to today in UTC).
- **Persisted locally** in `~/.emoji_mood_tracker.json` – no external services required.
- **Summary** command shows how many times each emoji was used.
- Fully tested, offline, and self‑contained.

## Installation
```bash
# Clone the repository (or copy the folder) and install dependencies (none beyond the Python stdlib).
cd utils/nightly-emoji-mood-tracker
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage
```bash
# Record today's mood
python -m src.mood_tracker add 😊

# Record a mood for a specific date
python -m src.mood_tracker add 😢 --date 2023-01-01

# Show a summary of all recorded moods
python -m src.mood_tracker summary
```

## Testing
```bash
python -m unittest discover -s tests
```

## License
MIT – see the root LICENSE file.
