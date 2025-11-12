# Silly Commit Message Generator

Generate whimsical commit messages from predefined templates and word lists. Perfect for adding a dash of fun to your git history.

## Features
- Randomly combines verbs, adjectives, and nouns.
- Simple CLI for quick message generation.
- Fully tested with deterministic mocks.

## Usage
```bash
python -m src.generate_message          # prints a random message
python -m src.generate_message 123      # optional seed for reproducibility
```

## Adding to your workflow
You can pipe the output directly into `git commit -m "$(python -m src.generate_message)"`.
