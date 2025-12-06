# Nightly Emoji Commit Suggester 🌙✨

Ever stare blankly at your commit message, wishing for that perfect emoji to encapsulate its essence? The Nightly Emoji Commit Suggester is here to sprinkle a little magic (and consistency!) into your commit history. This whimsical utility analyzes your commit message and suggests a relevant emoji, helping you maintain a more expressive and delightful repository log.

## ✨ Features

*   **Keyword-based Suggestions**: Intelligently maps common commit keywords (e.g., `feat`, `fix`, `docs`) to a curated list of emojis.
*   **CLI Friendly**: Easily integrate into your pre-commit hooks or use directly from your terminal.
*   **Lightweight & Self-contained**: A single Python script with no external dependencies.

## 🚀 How to Use

1.  **Navigate to the utility directory**:
    ```bash
    cd utils/nightly-emoji-commit-suggester
    ```

2.  **Run the suggester with your commit message**:
    ```bash
    python src/emoji_suggester.py "feat: Add new user authentication module"
    # Expected output: ✨
    ```

    ```bash
    python src/emoji_suggester.py "fix: Resolve critical bug in payment processing"
    # Expected output: 🐛
    ```

    ```bash
    python src/emoji_suggester.py "docs: Update README with new usage instructions"
    # Expected output: 📚
    ```

    If no specific emoji is found, it will return an empty string.

## 🛠️ Integration Example (Pre-commit Hook)

You can integrate this into a Git pre-commit hook to automatically suggest an emoji or even prepend it to your commit message.

Create a file `.git/hooks/pre-commit` (if it doesn't exist) and add:

```bash
#!/bin/sh
#
# An example hook script to prepend an emoji to the commit message.
#

COMMIT_MSG_FILE=$1
COMMIT_MESSAGE=$(cat "$COMMIT_MSG_FILE")

# Path to the emoji suggester script
EMOJI_SUGGESTER_SCRIPT="utils/nightly-emoji-commit-suggester/src/emoji_suggester.py"

# Check if the script exists and is executable
if [ ! -f "$EMOJI_SUGGESTER_SCRIPT" ]; then
    echo "Warning: Emoji suggester script not found at $EMOJI_SUGGESTER_SCRIPT"
    exit 0
fi

# Get suggested emoji
SUGGESTED_EMOJI=$(python "$EMOJI_SUGGESTER_SCRIPT" "$COMMIT_MESSAGE")

# Prepend emoji if found and not already present
if [ -n "$SUGGESTED_EMOJI" ] && ! echo "$COMMIT_MESSAGE" | grep -q "^$SUGGESTED_EMOJI"; then
    echo "$SUGGESTED_EMOJI $COMMIT_MESSAGE" > "$COMMIT_MSG_FILE"
    echo "Emoji '$SUGGESTED_EMOJI' prepended to commit message."
fi

exit 0
```

Make sure the hook is executable: `chmod +x .git/hooks/pre-commit`.

Now, when you commit, an emoji will be automatically suggested and prepended if a keyword is found!
