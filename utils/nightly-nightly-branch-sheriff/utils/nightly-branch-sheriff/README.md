# Nightly Branch Sheriff

**Purpose**: Identify stale Git branches in a repository based on the age of their last commit.

- **Why?** Over time, feature branches pile up, cluttering the repo and confusing contributors. This utility helps you spot branches that haven’t seen activity for a configurable number of days.
- **How?** Feed it a JSON‑serialisable list of `(branch_name, last_commit_iso)` tuples (or let it read `git for-each-ref` output). It returns a list of branch names that exceed the age limit.
- **Offline & deterministic** – no network calls, pure Python 3.11, no external dependencies.

## Installation

Copy the folder into your repository under `utils/nightly-branch-sheriff/`. No additional packages are required.

## Usage

```bash
python -m utils.nightly-branch-sheriff.src.branch_sheriff \
    --branches "[(\"feature/foo\", \"2023-09-01T12:00:00Z\"), (\"bugfix/bar\", \"2024-10-10T08:30:00Z\")]" \
    --max-age-days 30
```

The script prints a JSON array of stale branch names.

## Testing

Run the bundled tests with:

```bash
python -m unittest discover utils/nightly-branch-sheriff/tests
```

All tests are deterministic and use mocks; they never touch a real Git repository.
