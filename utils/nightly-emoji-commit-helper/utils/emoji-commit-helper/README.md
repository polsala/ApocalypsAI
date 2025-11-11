# Emoji Commit Helper

Add a dash of personality to your Git history!
`emoji-commit-helper` scans your commit message for keywords and suggests an emoji to prepend.

## Features

- Zero‑dependency, pure Python 3.11
- Simple keyword‑to‑emoji mapping (customizable)
- Works offline – no network calls

## Installation & Usage

```bash
# Run directly (no installation needed)
python -m utils.emoji-commit-helper.src.emoji_commit_helper "fix bug in parser"
# => 🐛 fix bug in parser
```

Or install as a module:

```bash
pip install .
emoji-commit-helper "add new feature to API"
# => ✨ add new feature to API
```

## How it works

The script looks for known keywords (e.g., `fix`, `add`, `remove`, `docs`) and returns the corresponding emoji. If no keyword matches, it falls back to `🔧`.

## License

MIT
