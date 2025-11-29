# Emoji Annotator

`emoji-annotator` is a lightweight, zero‑dependency Python 3.11 library that scans a string and appends an appropriate emoji to each recognized word.

## Features
- Deterministic, offline – no network calls.
- Simple static mapping (easy to extend).
- Small footprint – just a single function.

## Installation
```bash
# The utility is self‑contained; copy the folder into your project or install via pip if you package it.
```

## Usage
```python
from emoji_annotator import annotate

msg = "I love coffee and cats"
print(annotate(msg))
# Output: I ❤️ coffee ☕ and cats 🐱
```

## Extending the Mapping
Edit `src/annotator.py` and modify the `EMOJI_MAP` dictionary.
