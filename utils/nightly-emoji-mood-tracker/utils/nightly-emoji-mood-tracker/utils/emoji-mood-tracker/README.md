# Emoji Mood Tracker

A tiny, self‑contained utility that helps you record how you feel each day using emojis and later review a week‑long mood summary.

## Features

- **Add a mood** for any ISO date (`YYYY‑MM‑DD`).
- **Weekly summary** starting from a given date, showing emojis or a placeholder for missing entries.
- Persists data in a JSON file under your home directory (`~/.emoji_mood_tracker.json`).
- Pure Python 3.11, no external dependencies.

## Installation & Usage

```bash
# Clone the repository (or copy the folder) and navigate into it
cd utils/nightly-emoji-mood-tracker/utils/emoji-mood-tracker

# Run the CLI (Python 3.11 required)
python -m src.tracker add 2025-11-16 "😊"
python -m src.tracker summary 2025-11-10
```

The first command records a happy face for November 16 2025. The second prints a 7‑day window starting on November 10 2025.

## Development

Run the test suite with:

```bash
python -m unittest discover -s tests
```

All tests are deterministic and use in‑memory mocks, so they work offline.
