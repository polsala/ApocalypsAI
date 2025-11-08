# Nightly Emoji Commit Suggester

## 🌟 Overview

The `nightly-emoji-commit-suggester` is a whimsical-yet-useful utility designed to sprinkle a bit of fun and consistency into your commit messages. It analyzes your commit message for common keywords and suggests relevant emojis, helping you adhere to conventions (like Gitmoji or Conventional Commits with emojis) and make your commit history more visually engaging and informative.

## ✨ Features

- **Keyword-based Suggestions**: Scans your commit message for predefined keywords (e.g., `feat`, `fix`, `docs`, `test`) and proposes corresponding emojis.
- **Multiple Suggestions**: Can suggest multiple emojis if a message contains several relevant keywords.
- **CLI Friendly**: Easily integrated into commit hooks or CI/CD pipelines.

## 🚀 How to Use

1.  **Navigate**: Change into the `utils/nightly-emoji-commit-suggester/` directory.
2.  **Run**: Execute the `emoji_suggester.py` script with your commit message as an argument.

```bash
python src/emoji_suggester.py "feat: Add new user authentication module"
# Expected output: ✨

python src/emoji_suggester.py "fix(auth): Resolve critical bug in login flow"
# Expected output: 🐛

python src/emoji_suggester.py "docs: Update README with installation instructions"
# Expected output: 📚

python src/emoji_suggester.py "chore: Update dependencies and refactor old code"
# Expected output: ⚙️ ♻️
```

## 🛠️ Integration Example (Git Hook)

You can integrate this into a `prepare-commit-msg` Git hook to automatically suggest emojis before the commit message editor opens.

Create a file `.git/hooks/prepare-commit-msg` (make it executable `chmod +x`):

```bash
#!/bin/sh

COMMIT_MSG_FILE=$1

# Get the current commit message content
COMMIT_MESSAGE=$(cat "$COMMIT_MSG_FILE")

# Run the emoji suggester
# Ensure the path to the script is correct relative to your repository root
SUGGESTED_EMOJIS=$(python utils/nightly-emoji-commit-suggester/src/emoji_suggester.py "$COMMIT_MESSAGE")

# Prepend suggested emojis to the commit message file
if [ -n "$SUGGESTED_EMOJIS" ]; then
  echo "$SUGGESTED_EMOJIS $COMMIT_MESSAGE" > "$COMMIT_MSG_FILE"
fi
```

This will automatically add emojis to your commit message, which you can then review and modify before finalizing the commit.
