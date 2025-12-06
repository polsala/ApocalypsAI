# Nightly Emoji Mood Tracker

Utility that analyzes a piece of text and returns an emoji representing the overall mood. Uses a tiny built‑in sentiment word list, no external dependencies.

## Usage

```bash
python -m utils.nightly_emoji_mood_tracker.src.emoji_tracker "I love sunny days but hate traffic."
# Output: 😊
```

Or import:

```python
from utils.nightly_emoji_mood_tracker.src.emoji_tracker import detect_mood
print(detect_mood("..."))
```

## How it works

Counts occurrences of positive vs negative words. If positives > negatives → 😊, if negatives > positives → 😢, else 😐.

## Tests

Run with `pytest`:

```bash
pytest utils/nightly-emoji-mood-tracker/utils/emoji-mood-tracker/tests
```
