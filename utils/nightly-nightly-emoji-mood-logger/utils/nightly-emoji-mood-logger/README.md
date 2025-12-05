# Nightly Emoji Mood Logger

Utility that scans a plain‑text journal entry and returns a single emoji summarizing the mood. It uses a tiny built‑in sentiment word list, works offline, and has no external dependencies.

## How it works

- Reads the provided text.
- Counts occurrences of known positive and negative words.
- Calculates a simple sentiment score.
- Returns an emoji:
  - 😊 for overall positive mood
  - 😢 for overall negative mood
  - 😐 for neutral / mixed mood

## Usage

```bash
python -m src.mood_logger /path/to/journal.txt
```

Or as a library:

```python
from src.mood_logger import analyze_mood
emoji = analyze_mood("I had a wonderful day, but the rain made me sad.")
print(emoji)  # 😐
```

## Testing

Run the tests with:

```bash
python -m unittest discover -s tests
```
