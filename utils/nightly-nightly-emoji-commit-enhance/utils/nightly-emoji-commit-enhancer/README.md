# Emoji Commit Enhancer

A tiny utility that adds an emoji prefix to your git commit messages based on common keywords (e.g., `fix`, `add`, `remove`, `refactor`). It runs locally, has no external dependencies, and can be used as a pre‑commit hook or from the command line.

## Usage

```bash
python -m utils.nightly-emoji-commit-enhancer.src.enhancer "fix typo in README"
# Output: 🐛 fix typo in README
```

## How it works

The script scans the message for known keywords and selects the first matching emoji. If no keyword matches, the original message is returned unchanged.

## Installation

Copy the folder into your repository and run the script with Python 3.11.

## Testing

```bash
pytest utils/nightly-emoji-commit-enhancer/tests
```
