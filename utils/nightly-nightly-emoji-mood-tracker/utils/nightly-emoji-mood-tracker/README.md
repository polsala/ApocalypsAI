# Emoji Mood Tracker

Utility to record your mood each day using an emoji and later view a summary.

## Installation

```bash
pip install .
```

## Usage

```bash
# Add an entry for a specific date
python -m mood_tracker add 2025-11-26 😊

# Show a summary of all recorded moods
python -m mood_tracker summary
```

## How it works

The tool stores entries in a JSON file named `mood_data.json` located in the same directory as the script. Each entry is a tuple of `(date, emoji)`. Adding an entry for an existing date replaces the previous one.

## License

MIT © ApocalypsAI
