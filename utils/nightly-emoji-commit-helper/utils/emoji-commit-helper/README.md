# Emoji Commit Helper

A tiny utility that suggests an emoji to prepend to your git commit messages based on common keywords. No external dependencies, pure Python 3.11.

## Usage

```bash
python -m emoji_commit_helper "Add new feature for user login"
# Output: ✨ Add new feature for user login
```

Or as a script:

```bash
python utils/emoji-commit-helper/src/main.py "Fix bug in payment processing"
# Output: 🐛 Fix bug in payment processing
```

## How it works

The tool scans the commit message for known keywords and returns the corresponding emoji. If no keyword matches, it falls back to 🤖.

## Testing

Run:

```bash
python -m unittest discover utils/emoji-commit-helper/tests
```
