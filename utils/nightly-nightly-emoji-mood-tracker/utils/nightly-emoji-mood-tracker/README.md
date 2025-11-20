# Nightly Emoji Mood Tracker

A whimsical yet practical utility that lets you log your daily moods and see them represented as emojis.

## Features

- Convert common mood descriptors (e.g., "happy", "sad") to emojis.
- Store mood entries with dates.
- Generate a concise summary for any date range.
- Fully self‑contained Python 3.11 module.
- Deterministic offline tests using mocks.

## Usage

```python
from utils.nightly-emoji-mood-tracker.src.tracker import MoodTracker

tracker = MoodTracker()
tracker.add_mood('2025-11-01', 'happy')
tracker.add_mood('2025-11-02', 'tired')
print(tracker.get_summary('2025-11-01', '2025-11-02'))
```

## Running Tests

```bash
python -m unittest discover -s utils/nightly-emoji-mood-tracker/tests
```
