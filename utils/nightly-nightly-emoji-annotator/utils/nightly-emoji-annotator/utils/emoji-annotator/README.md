# Emoji Annotator

Utility that scans a text and inserts appropriate emojis after recognized keywords.

## Usage

```python
from src.annotator import annotate

text = "I love coffee and sunshine."
print(annotate(text))
# Output: I love coffee ☕ and sunshine 🌞.
```

## How it works

It uses a small built‑in mapping of keywords to emojis and replaces each occurrence with the word followed by the emoji.
