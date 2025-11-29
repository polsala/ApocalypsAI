# Emoji Annotator

**Utility name:** `emoji-annotator`

## What it does

`emoji-annotator` walks through a plain‑text string, looks for a handful of predefined keywords, and appends a corresponding emoji right after each match. It is deliberately lightweight, has no external dependencies, and can be used as a library function or a tiny CLI tool.

## Installation & usage

The utility is self‑contained – just copy the `src/` folder into your project or run it directly from the repository.

```bash
# Run as a module
python -m utils.emoji-annotator.src.annotator "I love coffee and cats"
```

Output:
```
I love coffee ☕ and cats 🐱
```

## API

```python
from utils.emoji-annotator.src.annotator import annotate

result = annotate("Happy birthday!")
# => "Happy birthday! 🎂"
```

## Testing

```bash
python -m unittest discover -s utils/nightly-emoji-annotator/utils/emoji-annotator/tests
```

All tests are deterministic and run offline.

## Extending

Add new keyword‑emoji pairs to the `KEYWORD_EMOJI_MAP` dictionary in `annotator.py`.
