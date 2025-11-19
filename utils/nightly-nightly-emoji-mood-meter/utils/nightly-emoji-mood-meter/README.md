# Nightly Emoji Mood Meter

Utility that converts a short piece of text into an emoji representing the overall mood, using simple keyword heuristics. Useful for adding a quick emotional tag to commit messages, issue titles, or chat snippets.

## Usage

```bash
python -m src.mood_meter "I love this new feature!"
# Output: 😊
```

Or import in Python:

```python
from src.mood_meter import get_mood_emoji
emoji = get_mood_emoji("I'm feeling sad about the bug.")
print(emoji)  # 😢
```

## How it works

The script scans the input for known mood keywords and returns a corresponding emoji. If no keywords match, it returns a thinking face 🤔.

## Tests

Run with `pytest`:

```bash
pytest -q
```
