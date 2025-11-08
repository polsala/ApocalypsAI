# Nightly Emoji Commit Enhancer

**Purpose**: Quickly add a relevant emoji to a git commit message to make your history more expressive and fun.

## Features
- Detects common keywords (e.g., *fix*, *add*, *remove*, *docs*, *refactor*) and prepends a matching emoji.
- Falls back to a generic 🎉 if no keyword matches.
- Stand‑alone Python 3.11 script, no external dependencies.

## Installation
```bash
# From the repository root
cd utils/nightly-emoji-commit-enhancer
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (empty, kept for future needs)
```

## Usage
```bash
python -m src.enhance "Add new feature for user login"
# Output: 🚀 Add new feature for user login
```

## Testing
```bash
python -m unittest discover -s tests
```
