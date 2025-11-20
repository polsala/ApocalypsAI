# Nightly Emoji Mood Meter

A tiny utility that scans a piece of text and returns a single emoji summarizing its mood.

## How it works

The script looks for positive and negative keywords (e.g., `happy`, `joy`, `sad`, `angry`). It counts occurrences and decides:

- More positive → 😄
- More negative → 😞
- Equal or none → 🤔

## Usage

```bash
python -m nightly_emoji_mood_meter "Your text here"
```

## API

```python
from nightly_emoji_mood_meter import mood_emoji
emoji = mood_emoji("I love sunny days!")
```

## Testing

Run the test suite with:

```bash
python -m unittest discover -s utils/nightly-emoji-mood-meter/tests
```
