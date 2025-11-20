# Emoji Mood Tracker

Utility to record your daily mood using emojis and view a summary.

## Usage

```sh
python -m mood_tracker add 😊   # add today's mood
python -m mood_tracker summary   # show counts per emoji
```

Data is stored in `mood_data.json` in the same directory as the script.

## Design

- **Self‑contained**: only the Python standard library.
- **Deterministic tests**: uses a temporary file and mocks the current date.
- **CLI friendly**: simple sub‑commands for adding a mood and printing a summary.
