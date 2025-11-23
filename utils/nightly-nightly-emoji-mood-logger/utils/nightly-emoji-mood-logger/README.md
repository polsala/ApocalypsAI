# Nightly Emoji Mood Logger

A tiny utility that infers a mood emoji from a short piece of text using simple keyword heuristics. Perfect for adding a quick sentiment tag to commit messages, daily logs, or chat snippets.

## Usage

```python
from src.logger import get_mood_emoji

text = "Implemented the new feature, feeling great!"
emoji = get_mood_emoji(text)
print(emoji)  # 😊
```

## How it works

- Scans the input for known happy, sad, and neutral keywords.
- Returns:
  - 😊 for happy
  - 😢 for sad
  - 😐 for neutral / no clear sentiment

## Testing

Run the tests with:

```bash
pytest -q
```
