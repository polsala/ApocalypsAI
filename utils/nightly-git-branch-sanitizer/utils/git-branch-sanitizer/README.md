# Git Branch Sanitizer

A lightweight, zero‑dependency Python utility that converts arbitrary strings into valid, kebab‑case Git branch names.

## Features

- Lower‑cases input
- Replaces spaces, underscores, and dots with hyphens
- Strips any character that is not alphanumeric or a hyphen
- Collapses consecutive hyphens
- Trims leading/trailing hyphens

## Installation

Copy the `src/` directory into your project or install via pip (once packaged).

```bash
# Example usage directly from the repository
python -m utils.git-branch-sanitizer src/sanitizer.py "My Feature/Branch v2"
```

## Usage

```bash
$ python -m utils.git-branch-sanitizer src/sanitizer.py "My Feature/Branch v2"
my-feature-branch-v2
```

## API

```python
from utils.git-branch-sanitizer.src.sanitizer import sanitize_branch_name

clean_name = sanitize_branch_name("My Feature/Branch v2")
```

## Testing

Run the bundled pytest suite:

```bash
pytest utils/git-branch-sanitizer/tests
```
