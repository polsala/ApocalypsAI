# Emoji Commit Enhancer

Utility that appends an emoji to a git commit message based on its conventional commit type (feat, fix, docs, style, refactor, test, chore). Helps developers quickly spot the nature of a change in logs.

## Installation

```bash
# The utility is self‑contained; just copy the folder or install via pip if packaged.
```

## Usage

```bash
# Pipe a commit message:

echo "feat: add login flow" | python -m utils.nightly-emoji-commit-enhancer.src.enhancer
# => "feat: add login flow 🚀"

# Or pass the message as an argument:

python -m utils.nightly-emoji-commit-enhancer.src.enhancer "fix: correct typo"
# => "fix: correct typo 🐛"
```

## How it works

- Parses the conventional commit type.
- Picks an emoji from a predefined list for that type.
- If the type is unknown, uses a generic sparkle ✨.

## Testing

Run the bundled tests with:

```bash
python -m unittest discover -s utils/nightly-emoji-commit-enhancer/tests
```
