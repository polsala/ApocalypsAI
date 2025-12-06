# Emoji Commit Enhancer

`emoji-commit-enhancer` is a lightweight, zero‑dependency Python utility that adds a fitting emoji to the beginning of a git commit message based on simple keyword detection.

## Features

- **Instant visual cue** – emojis convey the nature of a change at a glance.
- **Deterministic & offline** – no network calls, pure Python stdlib.
- **Easy to integrate** – can be used as a git `commit-msg` hook or called manually.

## Installation

```bash
# Clone the repository (or copy the folder into your project)
git clone https://github.com/polsala/ApocalypsAI.git
# Navigate to the utility folder
cd utils/emoji-commit-enhancer
# (Optional) create a virtual environment
python -m venv .venv && source .venv/bin/activate
# Install the package in editable mode
pip install -e .
```

## Usage

```bash
# As a module
python -m src.emoji_commit "Fix bug in parser"
# Output: 🐛 Fix bug in parser

# As a git commit‑msg hook (example)
# Save the following line in .git/hooks/commit-msg and make it executable:
#   python -m src.emoji_commit "$1"
```

## Development & Testing

```bash
# Run the test suite
pytest -q
```

## License

MIT © ApocalypsAI community
