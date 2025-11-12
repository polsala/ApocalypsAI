# Emoji Commit Generator

A lightweight Python utility that prefixes Git commit messages with an appropriate emoji based on the message content. It helps teams add a bit of personality to their history while staying deterministic and offline.

## Features
- Detects common commit‑type keywords (add, fix, docs, test, …).
- Returns the original message unchanged when no keyword matches.
- Simple CLI for quick usage.
- Zero external dependencies – pure Python 3.11.

## Installation
```bash
# From the repository root
cd utils/emoji-commit-generator
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (empty, kept for consistency)
```

## Usage
```bash
python -m src.generator "Add new feature"
# → ✨ Add new feature
```

## Mapping table
| Keyword | Emoji |
|---------|-------|
| add | ✨ |
| fix | 🐛 |
| remove | 🗑️ |
| update | 🔄 |
| refactor | 🛠️ |
| docs | 📚 |
| test | ✅ |
| ci | 🤖 |
| performance | ⚡ |
| security | 🔒 |

## Testing
```bash
python -m unittest discover -s tests
```
All tests run offline and are deterministic.
