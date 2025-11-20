# Emoji Mood Analyzer

**Utility name:** `nightly-emoji-mood-analyzer`

## What it does

Given a short piece of text, the tool returns a single emoji that best represents the overall mood of the input. It uses a lightweight keyword‑based heuristic, so it works completely offline and has zero runtime dependencies.

## Why it’s useful

- Add a dash of personality to automated logs or CI messages.
- Quickly surface the emotional tone of commit messages, issue titles, or chat snippets.
- Fun, whimsical, yet completely deterministic and testable.

## Installation & usage

The utility lives under `utils/nightly-emoji-mood-analyzer/`. It can be run directly with Python:

```bash
python -m utils.nightly-emoji-mood-analyzer.src.mood "I am so happy today!"
# → 😊
```

Or imported in your own code:

```python
from utils.nightly-emoji-mood-analyzer.src.mood import analyze_mood

emoji = analyze_mood("Feeling sad and lonely")
print(emoji)  # 😢
```

## How it works

A small dictionary maps groups of keywords to emojis. The input text is lower‑cased and split on whitespace; the first matching group determines the result. If no keywords match, a neutral thinking face (`🤔`) is returned.

## Testing

Run the bundled tests with:

```bash
python -m unittest discover utils/nightly-emoji-mood-analyzer/tests
```

All tests are deterministic and require no external resources.
