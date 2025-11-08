# Emoji Commit Message Generator

A whimsical yet practical utility that helps you prepend an appropriate emoji to your Git commit messages based on the keywords you provide.

## Features
- **Zero dependencies** – pure Python 3.11 standard library.
- Simple keyword‑to‑emoji mapping (customizable via the source).
- Command‑line interface for quick usage.
- Fully tested with deterministic offline unit tests.

## Installation
```bash
# Clone the repository (or copy the folder) and add it to your PATH
cd utils/emoji-commit-message-generator
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage
```bash
python -m src.emoji_commit "fix bug" "add feature"
# => 🐛 fix bug add feature
```

You can also import the library in your own scripts:
```python
from src.emoji_commit import generate_message
msg = generate_message(["refactor", "code"])  # => ♻️ refactor code
```

## Customising the Mapping
Edit the `EMOJI_MAP` dictionary in `src/emoji_commit.py` to add or change keyword‑emoji pairs.

## Testing
```bash
pytest -q
```
All tests run offline and are deterministic.
