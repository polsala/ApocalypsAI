# Emoji Mood Analyzer

A whimsical yet practical command‑line tool that reads a piece of text and returns a single emoji representing the overall mood.

## Features
- No external dependencies – pure Python 3.11.
- Deterministic sentiment analysis based on a curated word list.
- Works offline; perfect for scripts, GitHub Actions, or just for fun.

## Installation & Usage
```bash
# Clone the repository (or copy the folder) and run the script directly:
python -m utils.emoji-mood-analyzer.src.emoji_analyzer "I love sunny days!"
# → 😊
```

Or add the `src` directory to your `PYTHONPATH` and import the helper function:
```python
from emoji_analyzer import analyze_mood
print(analyze_mood("I hate rain"))  # 😞
```

## How it works
The analyzer tokenises the input, counts occurrences of known positive and negative words, and maps the resulting score to one of three emojis:
- Positive (`score > 0`) → 😊
- Negative (`score < 0`) → 😞
- Neutral (`score == 0`) → 😐

## Testing
Run the bundled tests with:
```bash
python -m pytest utils/emoji-mood-analyzer/tests
```
All tests are deterministic and require no network access.
