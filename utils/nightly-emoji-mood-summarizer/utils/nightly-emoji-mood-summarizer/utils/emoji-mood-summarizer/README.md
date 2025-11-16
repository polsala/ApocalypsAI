# Emoji Mood Summarizer

`emoji-mood-summarizer` is a lightweight Python utility that takes a collection of mood descriptors (e.g., "happy", "sad", "angry", "neutral") and returns a single emoji representing the most common mood.

## Features
- Simple, zero‑dependency implementation (Python 3.11 stdlib only).
- Deterministic output – the same input always yields the same emoji.
- Comes with a tiny test suite that runs offline.

## Usage
```bash
python -m emoji_mood_summarizer "happy" "sad" "happy"
# → 😊
```

You can also import the core function:
```python
from emoji_mood_summarizer import summarize_moods
emoji = summarize_moods(["angry", "angry", "neutral"])
print(emoji)  # 😠
```
