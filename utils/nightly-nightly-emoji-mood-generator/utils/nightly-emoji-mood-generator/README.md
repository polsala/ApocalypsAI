# Nightly Emoji Mood Generator

Utility that deterministically maps any date to a mood emoji. Useful for adding a whimsical daily mood indicator to logs, commit messages, or chat.

## Usage

```bash
python -m utils.nightly-emoji-mood-generator/src/emoji_mood.py [YYYY-MM-DD]
```

If no date is provided, today’s date is used.

## How it works

The utility hashes the ISO string of the date with SHA‑256, takes the integer value modulo the number of emojis, and returns the selected emoji. The mapping is deterministic and offline.

## Testing

Run `pytest` in the utility folder.
