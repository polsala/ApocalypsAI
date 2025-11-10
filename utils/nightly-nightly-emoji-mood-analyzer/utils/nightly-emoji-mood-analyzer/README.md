# Nightly Emoji Mood Analyzer

A whimsical yet practical utility that reads a line of text and returns the most appropriate mood **emoji** based on a small keyword dictionary.

## Features
- Zero‑dependency, pure Python 3.11.
- Simple CLI: `python -m emoji_mood_analyzer "I love this!"`
- Extensible mapping dictionary.
- Deterministic offline tests.

## Installation & Usage
```bash
# Clone the repository (or just copy this folder)
cd utils/nightly-emoji-mood-analyzer
python -m src.emoji_mood_analyzer "I am feeling great today!"
# → 😊
```

## How it works
The script lower‑cases the input, scans for known keywords, and returns the first matching emoji. If no keyword matches, it falls back to a thinking face (🤔).

## Testing
```bash
python -m unittest discover -s tests
```
All tests run offline and use mocks where needed.
