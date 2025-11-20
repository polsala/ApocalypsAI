# Emoji Mood Tracker

A whimsical yet practical utility that lets you log your daily mood using emojis and retrieve simple summaries. All data is stored locally in a JSON file, no external services required.

## Features

- Add a mood entry for any date.
- Optional short note per entry.
- Get a summary of moods over the last N days.
- Tiny CLI (`python -m src.mood_tracker`) for quick use.

## Installation

```bash
cd utils/nightly-emoji-mood-tracker
python -m venv .venv
source .venv/bin/activate
pip install .
```

(Or just run the script directly; it has no external dependencies.)

## Usage

```bash
# Add today's mood
python -m src.mood_tracker add --date 2025-11-20 --emoji 😊 --note "Feeling good"

# Show summary of last 7 days
python -m src.mood_tracker summary --days 7
```

## License

MIT
