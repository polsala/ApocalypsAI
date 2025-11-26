# Nightly Emoji Mood Tracker

A whimsical yet practical utility that lets you record your daily mood using an emoji and later view a quick summary of recent moods.

## Features
- **Add a mood entry** for a specific date (defaults to today).
- **Summarize** the last *N* days, showing how many times each emoji was used.
- Stores data in a tiny JSON file (`.mood_tracker.json`) in the user's home directory, so it persists across runs.
- Fully self‑contained Python 3.11 script with no external dependencies.

## Installation & Usage
```bash
# Clone the repository (or copy the utils folder) and navigate to the utility
cd utils/nightly-emoji-mood-tracker
python -m src.mood_tracker add 😄          # Add today's mood
python -m src.mood_tracker add 2025-11-20 😢  # Add mood for a specific date
python -m src.mood_tracker summary 7      # Show summary for the last 7 days
```

## Development
Run the test suite with:
```bash
python -m pytest tests
```

---
*Created by the ApocalypsAI Nightly Integrator.*
