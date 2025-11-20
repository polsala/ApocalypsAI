# Nightly Emoji Mood Tracker

Utility to record, retrieve, and analyze daily moods using emojis.

## Features

- **Record** an emoji for any date.
- **Query** the mood for a specific day.
- **Analyze** the most common mood.
- **Calculate** the longest consecutive‑day streak with recorded moods.

All data is persisted in a tiny JSON file, making the tool completely offline and deterministic.

## Usage (Python API)

```python
from pathlib import Path
from datetime import date
from utils.nightly_emoji_mood_tracker.src.mood_tracker import MoodTracker

# Initialise the tracker (it will create the file if missing)
tracker = MoodTracker(Path("./mood_data.json"))

# Record today's mood
tracker.set_mood(date.today(), "😀")

# Retrieve a mood
print(tracker.get_mood(date(2023, 1, 1)))

# Most common mood
print(tracker.most_common())  # -> ("😀", 5)

# Longest streak
print(tracker.longest_streak())
```

## Running the tests

```bash
python -m unittest discover -s utils/nightly-emoji-mood-tracker/tests
```
