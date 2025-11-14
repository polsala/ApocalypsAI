# Emoji Commit Generator

A whimsical‑yet‑useful utility that proposes an emoji prefix for your Git commit messages based on common keywords.

## Features

- **Zero dependencies** – pure Python 3.11 standard library.
- **Deterministic mapping** – offline, no network calls.
- **CLI** – `python -m emoji_commit "Add new feature"` prints `✨ Add new feature`.

## Installation

Copy the folder into your repository and run the script directly:

```bash
python -m utils/nightly-emoji-commit-generator/src/main "Fix typo in README"
```

## How it works

The utility scans the commit message for known keywords (e.g., `fix`, `add`, `docs`) and returns the corresponding emoji. If no keyword matches, it falls back to 🎉.

## Development

Run the test suite with:

```bash
python -m unittest discover utils/nightly-emoji-commit-generator/tests
```
