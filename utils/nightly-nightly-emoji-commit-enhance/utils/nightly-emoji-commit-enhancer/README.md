# Nightly Emoji Commit Enhancer

## Summary
A whimsical yet practical command‑line tool that prepends an appropriate emoji to a Git commit message based on its content. It helps developers quickly spot the nature of a change in `git log` while keeping the commit history readable.

## Features
- Detects common keywords (e.g., `fix`, `add`, `remove`, `refactor`, `docs`, etc.)
- Falls back to a default sparkle emoji for uncategorised messages
- Idempotent – if the message already starts with an emoji, it leaves it untouched
- Zero external dependencies; pure Python 3.11

## Installation
```bash
# From the repository root
cd utils/nightly-emoji-commit-enhancer
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

## Usage
```bash
# Directly via the module
python -m src.enhancer "Fix typo in README"
# → 🛠️ Fix typo in README

# As a script (make it executable)
chmod +x src/enhancer.py
./src/enhancer.py "Add new feature X"
# → ➕ Add new feature X
```

## Testing
```bash
python -m unittest discover -s tests
```
All tests run offline and are deterministic.

## License
MIT – see the repository LICENSE file.
