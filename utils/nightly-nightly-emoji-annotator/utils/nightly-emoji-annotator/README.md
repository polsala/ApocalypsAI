# Nightly Emoji Annotator

Utility that scans a piece of text and appends appropriate emojis based on detected sentiment keywords. Useful for adding a touch of fun to logs, chat messages, or commit messages.

## Usage

```bash
python -m nightly_emoji_annotator "I am happy but also a bit sad"
# Output: I am happy 😊 but also a bit sad 😢
```

## Implementation

- Simple keyword‑based sentiment detection.
- No external dependencies beyond the Python standard library.

## Tests

Run with:

```bash
python -m unittest discover utils/nightly-emoji-annotator/tests
```
