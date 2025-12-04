# Nightly Branch Sanitizer

Utility to transform arbitrary strings into Git‑compatible branch names.

## Features

- Lower‑case conversion
- Replace spaces and underscores with hyphens
- Remove characters other than alphanumerics and hyphens
- Collapse multiple hyphens
- Trim leading/trailing hyphens

## Usage

```bash
python utils/nightly-branch-sanitizer/src/sanitizer.py "My Feature #1!"
# => my-feature-1
```

## API

```python
from sanitizer import sanitize_branch
```

`sanitize_branch(name: str) -> str` returns a sanitized branch name.
