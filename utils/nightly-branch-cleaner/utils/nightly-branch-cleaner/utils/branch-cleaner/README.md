# Branch Cleaner

A whimsical yet practical utility that helps you keep your git repository tidy by identifying stale branches (no recent commits) and optionally deleting them. Works offline; you provide a mapping of branch names to their last commit dates.

## Usage

```python
from branch_cleaner import get_stale_branches, delete_branches

branches = {
    "feature/old": "2022-01-15T12:00:00Z",
    "main": "2024-10-01T08:30:00Z",
}

# Find branches older than 180 days
stale = get_stale_branches(branches, days_threshold=180)

# Mock‑delete them (returns the list of names)
deleted = delete_branches(stale)
print(f"Deleted: {deleted}")
```

The utility is pure Python, has no external git calls, and is safe to run in CI pipelines.
