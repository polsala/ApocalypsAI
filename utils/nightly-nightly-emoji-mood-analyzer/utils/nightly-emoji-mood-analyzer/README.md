# Emoji Mood Analyzer

Utility that determines the overall mood of a piece of text based on the emojis it contains.

## How it works

- Scans the input string for known emojis.
- Each emoji contributes to a mood bucket (`happy`, `sad`, `angry`).
- Returns the mood with the highest score, or `neutral` if none found or scores are tied.

## Usage

```bash
python -m utils.nightly-emoji-mood-analyzer.src.analyzer "I love this! 😊😊"
# Output: happy
```

## API

```python
from utils.nightly-emoji-mood-analyzer.src.analyzer import analyze_mood

mood = analyze_mood("I'm so angry! 😡")
print(mood)  # angry
```

## Tests

Run with `pytest`:

```bash
pytest utils/nightly-emoji-mood-analyzer/tests
```
