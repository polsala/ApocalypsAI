# Emoji Translator Utility

## Overview

`emoji-translator` is a tiny, self‑contained Python utility that scans a piece of text and replaces a handful of predefined words with their emoji equivalents.  It’s perfect for sprinkling a little personality into commit messages, chat logs, or any plain‑text content.

## Features

- **Deterministic mapping** – a fixed dictionary ensures the same input always yields the same output.
- **Case‑insensitive** – words are matched regardless of capitalization.
- **Preserves punctuation and whitespace** – only whole words are swapped.
- **CLI & library usage** – import `translate` in your code or run the script directly.

## Installation

The utility is completely self‑contained; just copy the folder into your repository and run it with Python 3.11.

```bash
cd utils/nightly-emoji-translator/utils/emoji-translator
python src/translator.py "I love my cat"
```

## Usage

### As a library

```python
from src.translator import translate

print(translate("I love pizza and coffee"))
# Output: I ❤️ 🍕 and ☕
```

### As a CLI

```bash
# Pass the text as arguments
python src/translator.py I love the star
# Output: I ❤️ the ⭐

# Or pipe from stdin
echo "Smile at the sun" | python src/translator.py
# Output: Smile at the ☀️
```

## Extending the Dictionary

Edit `src/translator.py` and modify the `EMOJI_MAP` dictionary to add or change mappings.

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/nightly-emoji-translator/utils/emoji-translator/tests
```
