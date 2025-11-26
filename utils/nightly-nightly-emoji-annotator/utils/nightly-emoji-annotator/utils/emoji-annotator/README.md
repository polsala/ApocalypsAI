# Emoji Annotator

`emoji-annotator` is a tiny, self‑contained Python utility that takes a plain‑text sentence and appends a random emoji to **each word**. It can be used from the command line or imported as a library.

## Features
- Pure‑Python, no external dependencies.
- Deterministic output when a seed is supplied (useful for testing).
- Simple CLI: `python -m emoji_annotator "Your text here"`.

## Installation
Just copy the `utils/nightly-emoji-annotator` folder into your repository. No additional packages are required.

## Usage
```bash
# As a module
python -m emoji_annotator "Hello world"
# Example output (emoji selection is random)
# Hello 🌟 world 🚀

# As a library
from emoji_annotator import annotate
print(annotate("Hello world", seed=42))
```

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/nightly-emoji-annotator/utils/emoji-annotator/tests
```
