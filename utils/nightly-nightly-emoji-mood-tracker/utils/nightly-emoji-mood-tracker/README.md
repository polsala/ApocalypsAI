# Emoji Mood Tracker

Utility that maps a short piece of text to an emoji representing its overall mood.

## Features

- No external dependencies.
- Simple keyword‑based sentiment heuristic.
- CLI: `python -m emoji_mood "I love this!"` prints 😊

## Installation

Copy the `src/` folder into your project or run directly.

## Usage

```python
from emoji_mood import get_mood_emoji

print(get_mood_emoji("I am feeling great today!"))  # 😊
```

## CLI

```bash
python -m emoji_mood "Your text here"
```

## Tests

Run `pytest` in the `tests/` directory.
