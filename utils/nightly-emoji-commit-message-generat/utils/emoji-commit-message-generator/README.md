# Emoji Commit Message Generator

A whimsical yet practical command‑line tool that turns a plain commit description into a commit message prefixed with a fitting emoji.

## Features
- Detects common commit keywords (e.g., `fix`, `add`, `remove`, `docs`, `refactor`, `test`).
- Maps each keyword to a representative emoji.
- Falls back to a generic sparkle emoji for unknown contexts.
- Zero external dependencies – pure Python 3.11.

## Installation
```bash
# From the repository root
cd utils/emoji-commit-message-generator
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage
```bash
emoji-commit "Add user authentication"
# ➕ Add user authentication

emoji-commit "Fix login bug"
# 🐛 Fix login bug
```

## Development
Run the test suite with:
```bash
pytest -q
```

## License
MIT © ApocalypsAI
