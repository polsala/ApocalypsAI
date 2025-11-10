# Emoji Commit Helper

A whimsical yet practical utility that suggests an emoji to prepend to your Git commit messages based on the content of the message.

## Features

- **Zero‑dependency** Python 3.11 script.
- Detects common commit intents (feature, bug‑fix, docs, refactor, tests, etc.) and maps them to an appropriate emoji.
- Simple CLI: `python -m emoji_commit_helper "Add new login endpoint"` → `🚀 Add new login endpoint`
- Fully documented and unit‑tested.

## Installation

```bash
# Clone the repository (or copy the folder) and add it to your PATH
cd utils/emoji-commit-helper
python -m venv .venv
source .venv/bin/activate
pip install -e .
```

> **Note**: The utility is self‑contained; no external services are required.

## Usage

```bash
python -m emoji_commit_helper "Fix typo in README"
# Output: 🐛 Fix typo in README
```

You can also import the helper in your own scripts:

```python
from src.emoji_commit_helper import suggest_emoji
print(suggest_emoji("Add unit tests for parser"))
# 🚀 Add unit tests for parser
```

## Development & Testing

Run the test suite with:

```bash
python -m pytest utils/emoji-commit-helper/tests
```

---

*Happy committing!*
