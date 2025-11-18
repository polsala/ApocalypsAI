# Nightly Emoji Mood Logger

Utility that scans a short piece of text and returns an emoji representing the overall mood. It uses a lightweight keyword‑based approach, making it fast, offline, and deterministic—perfect for quick mood‑tracking in scripts or commit messages.

## Usage

```python
from src.logger import get_mood_emoji

emoji = get_mood_emoji("I finally fixed the bug, feeling great!")
print(emoji)  # 😄
```

## How it works

A small dictionary maps mood‑related keywords to emojis. The function lower‑cases the input, counts occurrences of each keyword set, and returns the emoji with the highest score. If no keywords match, a neutral face is returned.

## Tests

Run the bundled tests with:

```bash
python -m unittest discover -s tests
```
