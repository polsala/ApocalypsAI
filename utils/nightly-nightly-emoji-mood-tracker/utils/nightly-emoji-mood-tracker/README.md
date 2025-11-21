# Nightly Emoji Mood Tracker

A whimsical yet practical command‑line tool that lets you record your mood with an emoji and later view a quick summary of how often each emoji was used.

## Features

- **Add a mood entry**: `python -m mood_tracker add "😊"`
- **Show summary**: `python -m mood_tracker summary`
- Stores data in a tiny JSON file (`.emoji_mood_log.json`) in the current working directory (or a custom path via `EMOJI_MOOD_LOG` env var).
- No external dependencies – pure Python 3.11 standard library.
- Fully tested with deterministic, offline unit tests.

## Installation

Copy the `utils/nightly-emoji-mood-tracker` folder into your repository and run the script directly with Python 3.11.

```bash
python -m utils/nightly-emoji-mood-tracker/src/mood_tracker add "😎"
python -m utils/nightly-emoji-mood-tracker/src/mood_tracker summary
```

## Usage

```bash
# Add a mood entry (any emoji string)
python -m mood_tracker add "😊"

# Show a summary of recorded emojis
python -m mood_tracker summary
```

## Testing

Run the tests with `pytest`:

```bash
pytest utils/nightly-emoji-mood-tracker/tests
```

The tests use a temporary directory and mock the log file location, ensuring they never touch real user data.
