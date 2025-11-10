# Emoji Mood Tracker

Utility to log your daily mood using emojis and view a summary.

## Installation

```bash
pip install .
```

## Usage

```bash
python -m src.mood_tracker add 😊
python -m src.mood_tracker summary
```

## Files

- `src/mood_tracker.py` – core logic and CLI.
- `mood_log.json` – created in the current directory to store entries.
