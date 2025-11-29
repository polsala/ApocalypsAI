# Nightly Emoji Mood Tracker

A lightweight, self‑contained Python utility for tracking your daily mood and getting a quick emoji summary.

## Features

- Record a mood for any date (`happy`, `sad`, `angry`, `neutral`).
- Retrieve the emoji that represents a specific day's mood.
- Get a concise emoji summary of all recorded days.
- Pure Python 3.11, no third‑party dependencies.

## Installation

```bash
# Clone the repository (or copy the folder) and install the utility in editable mode
pip install -e utils/nightly-emoji-mood-tracker
```

## Usage

```bash
# Add a mood entry
python -m nightly_emoji_mood_tracker add 2025-11-29 happy

# Show the emoji for a specific date
python -m nightly_emoji_mood_tracker show 2025-11-29

# Print a one‑line summary of all recorded moods
python -m nightly_emoji_mood_tracker summary
```

## Development

Run the test suite with:

```bash
pytest utils/nightly-emoji-mood-tracker/tests
```

## License

MIT © ApocalypsAI
