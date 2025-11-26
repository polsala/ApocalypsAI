# Nightly Emoji Mood Meter

Utility that converts a short text into a mood emoji based on simple keyword heuristics. Great for adding a dash of fun to logs, commit messages, or chat.

## Usage

```bash
python -m nightly_emoji_mood_meter "I finally fixed the bug!"
# Output: 😊
```

## How it works

- Looks for **angry** words → 😡
- Looks for **positive** words → 😊
- Looks for **negative** words → 😞
- If none match → 🤔

The matching is case‑insensitive and uses a small hard‑coded keyword list.

## Files

- `src/mood_meter.py` – core implementation and CLI entry point.
- `tests/test_mood_meter.py` – deterministic unit tests.
