# Nightly Emoji Mood Tracker

**Purpose**: Turn any calendar date into a fun emoji that reflects the "mood" of the day. The mapping is deterministic and offline, making it safe for CI environments.

## How it works
- The utility defines a fixed mapping from the day of the week to an emoji.
- `get_mood(date: datetime.date) -> str` returns the emoji for the supplied date.
- A small CLI wrapper (`python -m emoji_mood <YYYY-MM-DD>`) prints the emoji to stdout.

## Example
```bash
$ python -m emoji_mood 2025-12-25
🎄
```

## Files
- `src/emoji_mood.py` – core implementation and CLI entry point.
- `tests/test_emoji_mood.py` – deterministic unit tests.

## License
MIT – see LICENSE in the repository root.
