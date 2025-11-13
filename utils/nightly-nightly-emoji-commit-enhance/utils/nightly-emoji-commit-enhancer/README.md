# Emoji Commit Enhancer

Utility that prepends an emoji to a git commit message based on detected keywords.

## Features

- Detects common prefixes (`fix`, `add`, `remove`, `docs`, `refactor`, `test`, `chore`) and maps them to emojis.
- Works as a library (`enhance_message`) and as a CLI (`python -m utils.nightly-emoji-commit-enhancer.src.enhance "message"`).
- No external dependencies; pure Python 3.11.

## Usage

```bash
python -m utils.nightly-emoji-commit-enhancer.src.enhance "fix typo in README"
# => "🐛 fix typo in README"
```

## Installation

Copy the folder into your repo and run the script directly or import the function.

## License

MIT
