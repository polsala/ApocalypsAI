# Emoji Mood Tracker

A whimsical yet practical command‑line tool that lets you record your daily mood as an emoji and later view a simple histogram of how often each emoji was used.

## Features
- **Add** today’s mood with a single command.
- **Show** a histogram of all recorded moods.
- Stores data locally in a JSON file (`~/.emoji_mood_tracker.json`).
- Zero external dependencies – pure Python 3.11.

## Installation
Copy the `src/` directory into your Python path or run the module directly:
```bash
python -m mood_tracker add 😊
python -m mood_tracker show
```

## Usage
```bash
# Record today’s mood (defaults to today’s date)
python -m mood_tracker add 😎

# Record a mood for a specific date (ISO format)
python -m mood_tracker add 😢 --date 2023-10-31

# Show a histogram of all recorded moods
python -m mood_tracker show
```

## Data Location
The utility stores its data in a JSON file at `~/.emoji_mood_tracker.json`. The file format is a simple mapping of ISO‑date strings to emoji strings, e.g.:
```json
{
  "2025-11-20": "😊",
  "2025-11-19": "😴"
}
```

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s tests
```
