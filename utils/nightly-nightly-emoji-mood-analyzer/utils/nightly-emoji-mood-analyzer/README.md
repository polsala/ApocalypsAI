# Nightly Emoji Mood Analyzer

Utility that takes a piece of text (e.g., a journal entry) and returns an emoji representing the overall mood. It uses a tiny keyword‑based sentiment dictionary, making it fast, deterministic, and offline.

## How it works

- **Positive words**: happy, joy, love, excellent, good, great, wonderful, fantastic, amazing, pleased
- **Negative words**: sad, angry, hate, terrible, bad, awful, horrible, upset, depressed, miserable
- **Score** = (#positive) – (#negative)
- **Emoji mapping**:
  - score > 0 → 😊
  - score < 0 → 😞
  - score = 0 → 😐

## Usage

```python
from src.mood_analyzer import analyze_mood, load_text_from_path

text = "I had a wonderful day but the weather was terrible."
emoji = analyze_mood(text)
print(emoji)  # 😐
```

Or from a file:

```python
emoji = analyze_mood(load_text_from_path("journal.txt"))
```

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/nightly-emoji-mood-analyzer/tests
```
