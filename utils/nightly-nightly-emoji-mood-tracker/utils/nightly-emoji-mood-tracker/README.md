# Emoji Mood Tracker

**nightly-emoji-mood-tracker**

A whimsical yet practical utility that lets you record your daily mood using an emoji and later view a quick summary of how often each mood was logged.

## Features
- Append a mood entry for any ISO‑formatted date.
- Persist entries in a lightweight JSON file (`data.json`).
- Retrieve a dictionary mapping each emoji to its occurrence count.
- Pure Python 3.11, no external dependencies.

## Usage Example
```python
from utils.nightly_emoji_mood_tracker.src.tracker import add_mood, get_summary

# Record some moods
add_mood("2025-11-19", "😊")
add_mood("2025-11-20", "😢")
add_mood("2025-11-21", "😊")

# Get a summary
print(get_summary())  # {'😊': 2, '😢': 1}
```

## Running the Tests
```bash
cd utils/nightly-emoji-mood-tracker
python -m pytest -q
```

The tests are deterministic and run entirely offline.
