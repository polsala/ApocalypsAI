# Nightly Emoji Mood Tracker

## Overview

`emoji-mood-tracker` converts a human‑readable mood description into a single emoji. It is deliberately lightweight, has zero external dependencies, and runs on any Python 3.11 interpreter.

## Usage

```bash
python -m emoji_mood_tracker "feeling productive"
# Output: 🚀
```

The utility ships with a built‑in mapping table that can be extended via the `--custom` flag pointing to a JSON file.

## Development

- **Source**: `src/mood_tracker.py`
- **Tests**: `tests/test_mood_tracker.py`
- **License**: MIT
