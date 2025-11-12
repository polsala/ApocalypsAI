# Emoji Commit Message Generator

A tiny Python utility that turns a short description of your changes into a git commit message prefixed with a fitting emoji.

## Features

- Simple keyword‑to‑emoji mapping.
- Works offline, no external APIs.
- Provides a `generate_commit_message` function and a small CLI.

## Installation

```bash
pip install .
```

*(The utility is self‑contained; just copy the `src` folder into your project.)*

## Usage

```bash
python -m utils.emoji-commit-message-generator.src.generate_commit "add user authentication"
# => "🔐 add user authentication"
```

## Adding New Keywords

Edit the `EMOJI_MAP` dictionary in `generate_commit.py`.

## License

MIT
