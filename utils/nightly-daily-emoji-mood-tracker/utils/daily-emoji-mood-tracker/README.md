# Daily Emoji Mood Tracker

## Overview

`daily-emoji-mood-tracker` is a tiny, self‑contained Python utility that parses a plain‑text mood log and prints a colorful emoji histogram. Each line in the log should be of the form:

```
YYYY-MM-DD: <mood>
```

Supported moods (case‑insensitive) and their emojis:

| Mood      | Emoji |
|-----------|-------|
| happy     | 😄   |
| sad       | 😢   |
| angry     | 😠   |
| excited   | 🤩   |
| neutral   | 😐   |
| confused  | 🤔   |
| love      | ❤️   |
| tired     | 😴   |

The tool aggregates the counts and prints a one‑line summary like:

```
😄 5 | 😢 2 | 🤩 3
```

## Installation & Usage

```bash
# Clone the repository (or copy the utils folder) and navigate to the utility
cd utils/daily-emoji-mood-tracker
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt  # (no external deps needed)

# Run the tracker on a mood log file
python -m utils.daily-emoji-mood-tracker.src.mood_tracker path/to/mood.log
```

## Testing

```bash
pytest utils/daily-emoji-mood-tracker/tests
```

The tests are deterministic and run offline.
