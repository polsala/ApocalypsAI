# Emoji Annotator

A tiny utility that adds relevant emojis to plain‑text sentences based on keyword detection. Perfect for spicing up commit messages, notes, or chat logs without leaving your terminal.

## Usage

```bash
python -m emoji_annotator src/annotator.py "I love coffee and coding"
# Output: I love coffee ☕ and coding 💻
```

Or pipe a file:

```bash
cat notes.txt | python -m emoji_annotator src/annotator.py
```

## How it works

A hard‑coded mapping of keywords to emojis is scanned; the first matching keyword in each word is replaced by the word followed by the emoji.
