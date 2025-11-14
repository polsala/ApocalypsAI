# git-merged-branch-cleaner

A whimsical yet practical utility that helps you clean up stale local Git branches that have already been merged into the repository's default branch (usually `main` or `master`).

## Features
- Detects branches merged into the default branch.
- Shows a concise list of such branches.
- Optional `--delete` flag to remove them in one go (dry‑run by default).
- No external dependencies beyond the Python standard library.

## Installation
```bash
# From the repository root
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt  # (no extra deps needed)
```

## Usage
```bash
# Dry‑run (default) – just list merged branches
python -m utils.git-merged-branch-cleaner

# Actually delete the merged branches
python -m utils.git-merged-branch-cleaner --delete
```

## How it works
The script runs `git branch --merged <default>` to find merged branches, filters out the default branch itself, and then either prints them or runs `git branch -d <branch>` for each.

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s utils/git-merged-branch-cleaner/tests
```
All tests are deterministic and use mocks; no real Git repository is touched.
