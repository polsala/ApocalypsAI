# Nightly Emoji Mood Tracker

A whimsical yet practical utility for tracking your daily mood with emojis.

## Features
- Log a mood for any date using a single emoji (e.g., `😊`, `😢`, `🤔`).
- Stores data in a lightweight JSON file (`.mood_log.json`) in the current working directory.
- Retrieve a summary of the last *N* days.
- Find the most common mood in a given window.

## Installation & Usage
```bash
# Clone the repository (or copy the folder) and install dependencies (none beyond the Python stdlib).
python -m utils.nightly-emoji-mood-tracker.src.mood_tracker --help
```

### CLI
```bash
# Add or update today's mood
python -m utils.nightly-emoji-mood-tracker.src.mood_tracker add 2023-10-31 😊

# Show the last 7 days summary
python -m utils.nightly-emoji-mood-tracker.src.mood_tracker summary --days 7

# Show the most common mood in the last 30 days
python -m utils.nightly-emoji-mood-tracker.src.mood_tracker common --days 30
```

## Development
Run the test suite with:
```bash
pytest utils/nightly-emoji-mood-tracker/tests
```

## License
MIT © ApocalypsAI
