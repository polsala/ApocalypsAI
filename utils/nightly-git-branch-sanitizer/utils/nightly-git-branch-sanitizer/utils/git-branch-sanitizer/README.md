# Git Branch Sanitizer

Utility to transform arbitrary strings into safe Git branch names.

## Features

- Lower‑cases the input.
- Replaces spaces and underscores with hyphens.
- Removes characters not allowed in branch names (keeps alphanumerics, hyphens, slashes, and dots).
- Collapses multiple hyphens.
- Strips leading/trailing hyphens or slashes.

## Usage

```sh
python -m git_branch_sanitizer "Feature: Add New UI"
# => feature-add-new-ui
```

Or as a module:

```python
from git_branch_sanitizer import sanitize_branch
print(sanitize_branch("Feature: Add New UI"))
```
