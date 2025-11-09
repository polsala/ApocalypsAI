# Daily Emoji Mood Tracker

A whimsical yet practical command‑line tool that lets you record your mood each day using an emoji (and an optional note). All data is stored locally in a JSON file, making the utility completely offline and deterministic.

## Features

- **Log a mood**: `python -m daily_emoji_mood_tracker log "😊" "Feeling great!"`
- **Show a summary**: `python -m daily_emoji_mood_tracker summary --last 5`
- Stores data in a user‑configurable location (defaults to `$HOME/.local/share/daily_emoji_mood_tracker.json`).
- No external dependencies – just the Python standard library.

## Installation

Copy the `utils/daily-emoji-mood-tracker` folder into your project and run the module directly with Python 3.11+:

```bash
python -m daily_emoji_mood_tracker --help
```

## Usage

```bash
# Log a mood (emoji required, note optional)
python -m daily_emoji_mood_tracker log "😴" "Too early for coffee"

# Show the last 3 entries (default is 5)
python -m daily_emoji_mood_tracker summary --last 3
```

## Testing

The utility ships with a small test suite that runs offline and uses temporary files to avoid touching your real data.

```bash
python -m unittest discover -s utils/daily-emoji-mood-tracker/tests
```

---

*Happy tracking!*
