# Emoji Replacer

**Utility name:** `emoji-replacer`

## What it does

`emoji-replacer` scans a piece of text and substitutes a set of classic emoticon shortcuts (e.g. `:)`, `:-)`, `:(`, `;-)`) with their corresponding Unicode emoji characters. It can be used as a library function or as a tiny CLI tool.

## Installation

The utility is self‑contained and requires only the Python 3.11 standard library.

```bash
# Clone the repository (or copy the folder) and run the script directly
python utils/emoji-replacer/utils/emoji-replacer/src/emoji_replacer.py "Hello :)"
```

## Usage (CLI)

```bash
python utils/emoji-replacer/utils/emoji-replacer/src/emoji_replacer.py "I am happy :) and sad :("
# → I am happy 😊 and sad 🙁
```

You can also pipe a file:

```bash
python utils/emoji-replacer/utils/emoji-replacer/src/emoji_replacer.py < input.txt > output.txt
```

## Usage (as a library)

```python
from utils.emoji-replacer.utils.emoji-replacer.src.emoji_replacer import replace_emoticons

text = "Good morning! :-)"
print(replace_emoticons(text))  # → Good morning! 😊
```

## Supported emoticons

| Emoticon | Emoji |
|----------|-------|
| `:)` `:-)` `:D` `:-D` | 😊 |
| `:(` `:-(` | 🙁 |
| `;)` `;-)` | 😉 |
| `:P` `:-P` | 😛 |
| `:O` `:-O` | 😮 |
| `:/` `:-/` | 😕 |
| `:'(` | 😢 |

Feel free to extend the mapping in `src/emoji_replacer.py`.
