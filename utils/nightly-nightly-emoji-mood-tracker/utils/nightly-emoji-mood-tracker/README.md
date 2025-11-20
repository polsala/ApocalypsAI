# Nightly Emoji Mood Tracker

Utility that scans a short piece of text and returns an emoji representing the overall mood. Useful for adding a quick emotional summary to logs, commit messages, or daily notes.

## Features

- No external dependencies, pure Python.
- Simple keyword‑based heuristic (happy, sad, angry, neutral).
- CLI: `python -m emoji_tracker "I love this project!"` prints 😊.

## Installation

Copy the `src/emoji_tracker.py` file into your project or run directly from this folder.

## Usage

```bash
python -m utils/nightly-emoji-mood-tracker/src/emoji_tracker "Feeling great today!"
# Output: 😊
```

## Testing

```bash
pytest utils/nightly-emoji-mood-tracker/tests
```
