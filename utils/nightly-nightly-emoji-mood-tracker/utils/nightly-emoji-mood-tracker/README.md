# Nightly Emoji Mood Tracker

## Overview
`emoji-mood-tracker` is a tiny, self‑contained Python utility that prints a single emoji reflecting the *mood* of the current moment. The mood is derived from:

1. **Time of day** – morning, afternoon, evening, night each have a base emoji set.
2. **Deterministic randomness** – the calendar date seeds a `random.Random` instance so the same day always yields the same emoji for a given hour range.

The tool is useful for:
- Adding a playful emoji to commit messages (`git commit -m "Fix bug 😊"`).
- Populating daily status updates.
- Any place you want a light‑hearted, reproducible mood indicator.

## Installation
```bash
# From the repository root
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt  # (no external deps needed)
```

## Usage
```bash
python -m utils.nightly-emoji-mood-tracker.src.mood
# → 🌞
```

You can also import the function in your own scripts:
```python
from utils.nightly-emoji-mood-tracker.src.mood import get_mood
print(get_mood())
```

## Testing
```bash
pytest utils/nightly-emoji-mood-tracker/tests
```

The test suite is deterministic and runs offline – it uses a fixed datetime to verify the output.
