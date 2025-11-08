# Branch Name Sanitizer

Utility to transform any string into a safe Git branch name using kebab‑case.

## Features

- Lower‑cases all characters
- Replaces spaces, underscores, and dots with hyphens
- Removes characters not allowed in Git refs (keeps alphanumerics and hyphens)
- Collapses multiple hyphens into a single one
- Strips leading/trailing hyphens

## Usage

```bash
python -m utils.branch-name-sanitizer.src.sanitizer "Feature: Add New UI!"
# => feature-add-new-ui
```

## API

```python
from utils.branch-name-sanitizer.src.sanitizer import sanitize_branch_name

sanitized = sanitize_branch_name("My Feature_1")
```

## Tests

Run with `pytest`:

```bash
pytest utils/branch-name-sanitizer/tests
```
