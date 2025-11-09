# Nightly Emoji Commit Suggester

## 🌟 Whimsical Utility for Expressive Commits 🌟

This utility, lovingly crafted by the ApocalypsAI Nightly Integrator, helps you add a touch of whimsy and clarity to your commit messages. It scans your proposed commit message for keywords and suggests relevant emojis, encouraging consistent and expressive commit hygiene across the repository.

Inspired by conventions like [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) and popular emoji guides, this tool aims to make your `git log` a more colorful and informative story of your project's evolution.

## ✨ How to Use

Simply pipe your commit message into the utility, or pass it as a command-line argument. It will output a list of suggested emojis, one per line, that you can then prepend or append to your commit message.

### Via Pipe:

```bash
echo "feat: Add new user authentication module" | python3 src/suggester.py
# Expected output:
# ✨
```

### Via Argument:

```bash
python3 src/suggester.py "fix: Resolve critical bug in payment processing"
# Expected output:
# 🐛
```

### Integrating with Git Hooks (Optional):

You can integrate this into a `prepare-commit-msg` git hook to automatically suggest emojis before you finalize your commit message. For example, in `.git/hooks/prepare-commit-msg`:

```bash
#!/bin/sh
COMMIT_MSG_FILE=$1

# Read the current commit message
COMMIT_MESSAGE=$(cat "$COMMIT_MSG_FILE")

# Get emoji suggestions
SUGGESTED_EMOJIS=$(python3 utils/nightly-emoji-commit-suggester/src/suggester.py "$COMMIT_MESSAGE")

# If suggestions exist, prepend them to the commit message
if [ -n "$SUGGESTED_EMOJIS" ]; then
  # Prepend emojis, then the original message
  echo "$SUGGESTED_EMOJIS $COMMIT_MESSAGE" > "$COMMIT_MSG_FILE"
fi
```

Remember to make the hook executable: `chmod +x .git/hooks/prepare-commit-msg`.

## 🛠️ Development

The utility is written in Python 3.11 and is self-contained. Tests are located in `tests/test_suggester.py` and can be run with `pytest`.

```bash
cd utils/nightly-emoji-commit-suggester
pytest
```
