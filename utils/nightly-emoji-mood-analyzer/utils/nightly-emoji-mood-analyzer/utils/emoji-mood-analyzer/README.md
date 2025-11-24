# Emoji Mood Analyzer

A whimsical utility that scans a piece of text and returns an appropriate emoji representing its overall mood. Uses simple keyword heuristics to classify sentiment as positive, neutral, or negative.

## Usage

```bash
python -m src.emoji_analyzer "I love sunny days!"
# 😊
```

## How it works

- Checks for presence of positive words (e.g., love, great, happy) → 😊
- Checks for negative words (e.g., hate, terrible, sad) → 😞
- Otherwise → 😐
