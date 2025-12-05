# Branch Name Sanitizer

Utility to transform arbitrary strings into safe Git branch names in kebab-case.

- Removes spaces and most punctuation, replacing them with hyphens.
- Collapses consecutive hyphens into a single one.
- Trims the result to a maximum of 50 characters.
- Guarantees the name starts with a letter (prepends `branch-` if needed).
- Provides a tiny CLI for quick ad‑hoc usage.

## Usage
```bash
python -m src.sanitizer "My Feature! #1"
# => my-feature-1
```

## API
```python
from src.sanitizer import sanitize_branch_name

clean_name = sanitize_branch_name(raw_name)
```
