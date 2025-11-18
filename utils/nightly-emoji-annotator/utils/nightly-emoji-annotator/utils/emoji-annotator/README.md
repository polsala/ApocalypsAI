# Emoji Annotator

**Utility name:** `emoji-annotator`

## Overview

`emoji-annotator` scans a piece of text and appends an appropriate emoji after each word that matches a small built‑in dictionary. It is deliberately lightweight, has no external dependencies, and runs on any Python 3.11 interpreter.

## Features

- Simple word‑to‑emoji mapping (hard‑coded, offline).
- Public function `annotate(text: str) -> str` for programmatic use.
- Command‑line interface:
  ```bash
  python -m utils.emoji-annotator.src.annotator "I love pizza"
  # → I 🍕 love ❤️ pizza 🍕
  ```
- Fully unit‑tested with deterministic mocks.

## Installation

Copy the folder into your repository (the generator does this automatically). No additional packages are required.

## Usage

```python
from utils.emoji-annotator.src.annotator import annotate

print(annotate("Good morning world"))
# Output: Good ☀️ morning 🌅 world 🌍
```

Or via CLI:

```bash
python -m utils.emoji-annotator.src.annotator "Happy birthday"
```

## Extending the Mapping

Edit the `WORD_EMOJI_MAP` dictionary in `src/annotator.py` to add or change mappings.
