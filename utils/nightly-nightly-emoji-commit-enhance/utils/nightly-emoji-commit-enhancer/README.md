# Emoji Commit Enhancer

A tiny utility that appends an appropriate emoji to a git commit message based on simple keyword heuristics. Helps make commit logs more readable and fun.

## Installation

```bash
pip install .
```

(Assuming you add this folder to `PYTHONPATH` or install as a package.)

## Usage

```bash
python -m utils.nightly-emoji-commit-enhancer.src.enhance "Add new login endpoint"
# Output: Add new login endpoint ✨
```

## How it works

- Looks for keywords like `fix`, `bug` → 🐛
- `add`, `feature`, `implement` → ✨
- `remove`, `delete`, `rm` → ❌
- Otherwise picks a random celebratory emoji.

## Testing

```bash
python -m unittest discover -s utils/nightly-emoji-commit-enhancer/tests
```
