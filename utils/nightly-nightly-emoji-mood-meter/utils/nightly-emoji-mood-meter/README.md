# Nightly Emoji Mood Meter

Utility that takes a short sentence and returns an emoji reflecting its mood.

## Usage
```bash
python -m src.mood_meter "I love sunny days!"
```
Will output:
```
😊
```

## Installation
Just ensure you have Python 3.11+ available. No external dependencies are required.

## How it works
The script tokenises the input, counts occurrences of a small built‑in list of positive and negative words, and chooses:
- 😊 for overall positive
- 😞 for overall negative
- 😐 for neutral or tied sentiment
