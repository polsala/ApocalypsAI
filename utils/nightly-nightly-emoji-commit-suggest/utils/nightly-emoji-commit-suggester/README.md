# Nightly Emoji Commit Suggester

A whimsical utility for the ApocalypsAI community that helps you add a touch of personality and consistency to your commit messages by suggesting relevant emojis based on common keywords.

## ✨ Why use it?

- **Expressive Commits**: Make your commit history more readable and visually engaging.
- **Consistency**: Encourage a standardized emoji usage across your team or personal projects.
- **Whimsical Fun**: Because even the apocalypse needs a little sparkle!

## 🚀 How to Use

This utility can be run from the command line, taking a commit message as input and outputting a list of suggested emojis.

### Installation (if standalone)

```bash
# No special installation needed if run within the ApocalypsAI ecosystem.
# If you want to run it standalone, ensure Python 3.11+ is installed.
```

### Example

```bash
python src/emoji_suggester.py "feat: Add new user authentication module"
# Output: ✨

python src/emoji_suggester.py "fix(auth): Resolve critical bug in login flow"
# Output: 🐛

python src/emoji_suggester.py "docs: Update README with new usage instructions"
# Output: 📚

python src/emoji_suggester.py "refactor: Clean up old database queries"
# Output: ♻️

python src/emoji_suggester.py "chore: Update dependencies"
# Output: 🧹 📦

python src/emoji_suggester.py "Initial commit"
# Output: 🎉

python src/emoji_suggester.py "Just a random commit"
# Output: (empty line if no matches)
```

## 🛠️ Configuration

The emoji mappings are hardcoded within `src/emoji_suggester.py`. Keywords are matched case-insensitively using whole word regex boundaries (`\b`) for accuracy.

## 🧪 Development & Testing

Run the tests using `unittest` (or `pytest` if installed) from the utility's root directory:

```bash
python -m unittest tests/test_emoji_suggester.py
```
