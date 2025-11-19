# Nightly Emoji Mood Tracker

A whimsical yet useful utility that prints an emoji representing the current time of day, giving you a quick visual cue of your "mood". Perfect for adding a touch of fun to your terminal or CI logs.

## Features

- **CLI**: `python -m mood_tracker` prints the appropriate emoji.
- **Library**: `get_mood_emoji(hour: int) -> str` returns the emoji for any hour (0‑23).
- **Deterministic tests**: Uses mocks to simulate different times.

## Usage

```bash
$ python -m mood_tracker
🌅  # sunrise emoji for early morning
```

## Installation

Copy the `src/` folder into your project or run directly from this utility.

## License

MIT
