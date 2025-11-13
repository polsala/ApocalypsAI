# Emoji Commit Annotator

A tiny utility that prepends an appropriate emoji to a git commit message based on simple keyword heuristics. Useful for adding a splash of personality to commit logs without external services.

## Features

- No network calls, pure Python 3.11.
- Deterministic mapping (no randomness).
- CLI: `python -m src.annotate "Your commit message"` prints the annotated message.

## Example

```bash
$ python -m src.annotate "fix typo in README"
🛠️ fix typo in README
```

## Installation

Copy the folder into your repository and run the script with Python 3.11.

## Testing

```bash
python -m unittest discover -s tests
```
