# Emoji Commit Message Generator

A tiny, self‑contained Python utility that turns a short commit description into a whimsical, emoji‑prefixed commit message.

## Features
- No external dependencies beyond the Python standard library.
- Deterministic keyword‑to‑emoji mapping (offline, no network calls).
- Simple CLI for quick usage:
  ```bash
  python -m emoji_commit "fix typo in README"
  # => 🛠️ fix typo in README
  ```

## How it works
The script contains a hard‑coded dictionary mapping common commit keywords (e.g., `fix`, `add`, `remove`, `refactor`) to emojis. When you provide a description, the first matching keyword determines the emoji prefix. If no keyword matches, a generic 📦 emoji is used.

## Installation & Usage
1. Clone the repository and navigate to the utility folder.
2. Run the module directly:
   ```bash
   python -m utils.emoji-commit-message-generator.src.emoji_commit "your description here"
   ```
3. Or import the function in your own scripts:
   ```python
   from utils.emoji-commit-message-generator.src.emoji_commit import generate_commit_message
   msg = generate_commit_message("add new feature")
   print(msg)  # 📦 add new feature
   ```

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/emoji-commit-message-generator/tests
```
All tests are deterministic and require no network access.
