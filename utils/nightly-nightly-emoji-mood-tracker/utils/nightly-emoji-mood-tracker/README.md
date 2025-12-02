# Nightly Emoji Mood Tracker

A whimsical yet practical utility for tracking your daily mood with emojis.

## Features

- **Log a mood** for any date using a single emoji (e.g., 😄, 😐, 😢).
- **Persist** data locally in a JSON file (`mood_log.json`).
- **Summarize** the last N days, showing counts per emoji and the most common mood.
- Pure Python 3.11, no external dependencies.

## Installation

Copy the `src/` folder into your project or add it to `PYTHONPATH`.

```bash
pip install .  # if you turn this into a package later
```

## Usage Example

```python
from mood_tracker import MoodTracker

tracker = MoodTracker()
tracker.add_entry('2025-12-01', '😄')
tracker.add_entry('2025-12-02', '😐')
tracker.add_entry('2025-12-03', '😄')

print(tracker.get_summary(days=7))
```

## API

### `MoodTracker(log_path: str = "mood_log.json")`
Creates a tracker. If the log file does not exist, it is created automatically.

### `add_entry(date: str, emoji: str) -> None`
Adds a mood entry. `date` must be in `YYYY‑MM‑DD` format. The emoji is stored as‑is.

### `get_summary(days: int = 30) -> dict`
Returns a dictionary with:
- `total_entries`: total number of logged moods in the window.
- `counts`: mapping of emoji → count.
- `most_common`: the emoji with the highest count (or `None` if no entries).

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/nightly-emoji-mood-tracker/tests
```
