# Emoji Commit Message Generator

A whimsical yet practical utility that converts a plain commit description into a commit message prefixed with an appropriate emoji.

## Features
- Keyword‑based emoji selection (bug, feature, docs, refactor, test, chore, etc.)
- Fallback to a generic emoji when no keyword matches
- Zero external dependencies – pure Python 3.11

## Installation
```bash
# Clone the repository (or copy the folder) and install the utility in a virtual environment
python -m venv .venv
source .venv/bin/activate
pip install -e utils/emoji-commit-message-generator
```

## Usage
```bash
python -m emoji_commit_message_generator "fix crash on empty input"
# → 🐛 Fix crash on empty input
```

## Development
Run the test suite with:
```bash
pytest utils/emoji-commit-message-generator/tests
```
