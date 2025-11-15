# Emoji Commit Helper

A whimsical yet practical utility that suggests an emoji to prepend to your Git commit messages based on the message content.

## Why?
Adding an emoji to a commit can instantly convey the nature of the change (e.g., a bug fix, a new feature, documentation updates). This helper automates the selection so you don’t have to think about which emoji to use.

## Installation
Simply copy the `utils/emoji-commit-helper` directory into your repository. No external dependencies are required beyond the Python standard library.

## Usage
```bash
python -m utils.emoji-commit-helper.src.emoji_helper "Your commit message here"
```
The script will print the suggested emoji followed by the original message, ready to be used in `git commit -m`.

### Example
```bash
$ python -m utils.emoji-commit-helper.src.emoji_helper "Fix race condition in scheduler"
🐛 Fix race condition in scheduler
```

## How it works
The helper scans the commit message for known keywords (e.g., `fix`, `add`, `docs`) and returns the first matching emoji. If no keyword matches, a generic light‑bulb emoji (`💡`) is used.

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/emoji-commit-helper/tests
```
All tests are deterministic and run offline.
