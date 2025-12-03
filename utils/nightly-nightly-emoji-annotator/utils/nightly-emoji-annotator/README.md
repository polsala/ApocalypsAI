# Nightly Emoji Annotator

Utility that scans a block of text and appends appropriate emojis to each sentence based on simple keyword heuristics. Useful for adding a touch of fun to logs, chat messages, or documentation.

## Usage

```bash
python -m nightly-emoji-annotator src/annotator.py "I love Python. It makes me happy!"
# Output: I love Python ❤️. It makes me happy! 😊
```

## How it works

- Splits text into sentences using punctuation.
- Looks for keywords (love, happy, sad, fire, etc.).
- Appends the corresponding emoji if a keyword is found.
- If multiple keywords match, the first in priority order is used.

## Extending

Add more keyword→emoji pairs in `EMOJI_MAP`.
