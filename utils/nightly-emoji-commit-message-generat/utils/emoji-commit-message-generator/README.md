# Emoji Commit Message Generator

A tiny, self‑contained Python utility that turns a short commit description into a git‑style commit message prefixed with an appropriate emoji.

## Why?
* Emojis make commit histories more readable at a glance.
* No external services – works completely offline.
* Deterministic mapping ensures the same input always yields the same emoji.

## Installation
```bash
# From the repository root
cd utils/emoji-commit-message-generator
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (empty – only stdlib)
```

## Usage
```bash
python -m src.emoji_commit "Add user authentication"
# => "🔐 Add user authentication"
```

You can also import the helper function in your own scripts:
```python
from src.emoji_commit import emoji_commit_message
msg = emoji_commit_message("Fix typo in README")
print(msg)  # 📝 Fix typo in README
```

## How it works
A small keyword‑to‑emoji map is consulted. The first matching keyword (case‑insensitive) determines the emoji. If no keyword matches, a generic 📦 emoji is used.

## Testing
```bash
pytest -q
```
All tests run offline and use no network calls.
