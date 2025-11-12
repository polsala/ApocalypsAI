# Emoji Commit Message Generator

A tiny Python utility that reads a commit message (or a short description) and returns a suitable emoji prefix to prepend to the message. It works entirely offline and requires no external services.

## Installation

```bash
pip install -r requirements.txt  # No external dependencies needed
```

## Usage

```bash
python -m emoji_commit_message_generator "Fix typo in README"
# Output: 🐛 Fix typo in README
```

## How it works

The script scans the input text for known keywords (e.g., `add`, `fix`, `remove`, `docs`, `test`, `refactor`) and selects an emoji from a predefined map. If no keyword matches, it falls back to the generic `🔧`.

## Testing

Run the test suite with:

```bash
pytest
```
