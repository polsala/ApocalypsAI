# Nightly Emoji Mood Tracker

A whimsical yet practical command‑line tool for tracking your daily mood with emojis.

## Features

- **Log a mood** for any date using a single emoji (e.g., `😊`, `😢`, `🤔`).
- **Persist data** locally in a JSON file (`~/.emoji_mood_tracker.json`).
- **Summarize** the count of each emoji you have logged.
- Zero external dependencies – pure Python 3.11 standard library.

## Installation

Copy the `utils/nightly-emoji-mood-tracker` folder into your repository and run the script directly:

```bash
python -m utils.nightly-emoji-mood-tracker.src.mood_tracker <command> [args]
```

## Usage

```bash
# Add a mood entry for today
python -m utils.nightly-emoji-mood-tracker.src.mood_tracker add 2025-11-27 😊

# Add a mood entry for a past date
python -m utils.nightly-emoji-mood-tracker.src.mood_tracker add 2025-11-20 😢

# Show a summary of all logged moods
python -m utils.nightly-emoji-mood-tracker.src.mood_tracker summary
```

## Development & Testing

Run the test suite with:

```bash
python -m unittest discover utils/nightly-emoji-mood-tracker/tests
```

The tests are deterministic and use a temporary file to avoid touching the real user data.
