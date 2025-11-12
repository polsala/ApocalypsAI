# Emoji Mood Analyzer

A tiny utility that maps input text to a mood emoji based on keyword heuristics. Useful for adding quick emotional context to commit messages, chat posts, or any short text.

## Usage

```bash
python -m emoji_mood_analyzer "I love this new feature!"
# Output: 😄
```

## How it works

The analyzer looks for keywords in the text (case‑insensitive). The first matching keyword determines the emoji. If no keywords match, a neutral face 😐 is returned.

## Adding keywords

Edit the `KEYWORD_EMOJI_MAP` dictionary in `src/analyzer.py` to add or change mappings.

## Tests

```bash
cd utils/emoji-mood-analyzer
pytest
```
