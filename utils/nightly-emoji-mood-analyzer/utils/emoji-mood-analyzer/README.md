# Emoji Mood Analyzer

## Overview

`emoji-mood-analyzer` is a lightweight, zero‑dependency Python utility that scans a string for known emojis and returns a simple mood label (`happy`, `sad`, `angry`, `love`, `neutral`).

It is useful for:
- Summarizing sentiment in community chat logs.
- Adding a quick mood badge to GitHub issues or PR comments.
- Fun analytics on emoji usage across a repository.

## Installation

```bash
# Clone the repository (or copy the folder) and install the utility in a virtualenv
python -m venv .venv
source .venv/bin/activate
pip install -e utils/emoji-mood-analyzer
```

## Usage

```bash
python -m emoji_mood_analyzer "I love this new feature! 😍🚀"
# Output: love
```

## API

```python
from emoji_mood_analyzer import analyze

mood = analyze("I'm so sad... 😢")
print(mood)  # -> "sad"
```

## Testing

Run the bundled tests with:

```bash
pytest utils/emoji-mood-analyzer/tests
```

## License

MIT © ApocalypsAI
