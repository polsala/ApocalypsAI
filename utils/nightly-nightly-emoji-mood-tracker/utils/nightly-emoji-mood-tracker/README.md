# Nightly Emoji Mood Tracker

## Overview

`nightly-emoji-mood-tracker` provides a simple function that analyses a short string and returns an emoji that best represents the sentiment of the text.

* **Why?** Quickly add a visual mood indicator to daily journals, commit messages, or any free‑form note.
* **How?** Keyword‑based matching – no external APIs, fully offline and deterministic.

## Usage

```bash
python -m src.emoji_mood "I had a fantastic day!"
# Output: 😊
```

Or import the function in your own code:

```python
from src.emoji_mood import get_mood_emoji

emoji = get_mood_emoji("Feeling a bit down today.")
print(emoji)  # 😢
```

## Testing

Run the test suite with:

```bash
python -m unittest discover -s tests
```

All tests are deterministic and require no network access.
