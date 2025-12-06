# Random Emoji Commit Generator

Generate fun commit messages with random emojis and concise action phrases.

## Installation

```bash
pip install .
```

*(The utility is self‑contained; you can also run it directly with Python.)*

## Usage

```bash
python -m random_emoji_commit_generator
```

or

```bash
python utils/random-emoji-commit-generator/src/main.py
```

Options:

- `--num-emojis N` – Number of emojis to prepend (default: 2).

## How it works

The script selects *N* random emojis from a curated list and combines them with a random short phrase (e.g., "Add feature").

## Testing

```bash
python -m unittest discover -s utils/random-emoji-commit-generator/tests
```
