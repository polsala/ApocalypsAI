# Emoji Mood Tracker

A tiny, offline‑only CLI utility that lets you log your daily mood using emojis and view simple statistics.

## Features

- Log a mood for a specific date (defaults to today) with any emoji.
- Store data in a JSON file in your home directory (`~/.emoji_mood_log.json`).
- Show a summary: total entries, most common emoji, and a chronological list.

## Installation

Copy the `src/mood_tracker.py` file somewhere on your `PATH` or run it via Python:

```bash
python -m emoji_mood_tracker.src.mood_tracker add 😊
python -m emoji_mood_tracker.src.mood_tracker stats
```

## Usage

```bash
# Add today's mood
python -m emoji_mood_tracker.src.mood_tracker add 😊

# Add mood for a specific date
python -m emoji_mood_tracker.src.mood_tracker add 😢 --date 2023-10-31

# Show statistics
python -m emoji_mood_tracker.src.mood_tracker stats
```

## License

MIT
