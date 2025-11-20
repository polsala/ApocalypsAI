# Git Branch Sanitizer

Utility to transform arbitrary strings into safe Git branch names.

## Features

- Lowercases input
- Replaces spaces and underscores with hyphens
- Removes characters not allowed in branch names (keeps alphanumerics, hyphens, slashes, and periods)
- Collapses multiple hyphens
- Strips leading/trailing hyphens

## Usage

```bash
python -m utils.git-branch-sanitizer.src.sanitizer "Feature: Add New UI!"
# => feature-add-new-ui
```

## API

```python
from utils.git-branch-sanitizer.src.sanitizer import sanitize_branch
sanitized = sanitize_branch("My Feature")
```
