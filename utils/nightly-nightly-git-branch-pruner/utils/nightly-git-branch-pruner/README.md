# nightly‑git‑branch‑pruner

A lightweight, self‑contained Python utility that helps keep your local Git repository tidy.

## What it does
- Detects all local branches that have been fully merged into `main` (or any base branch you specify).
- Prints a clean, colour‑coded list of those branches.
- **Optional**: deletes the merged branches with a `--delete` flag (dry‑run is the default).

## Why it’s useful
Developers often accumulate stale feature branches after merges. Running `git branch --merged` manually is easy, but forgetting to prune can clutter the repo and cause confusion. This script automates the safe part of that workflow and can be run as part of a nightly maintenance job.

## Installation & Usage
```bash
# Clone the repository (or copy the folder) and install the tiny runtime deps
pip install -r utils/nightly-git-branch-pruner/requirements.txt  # optional, only `rich` is needed

# Run the utility (dry‑run, just lists branches)
python utils/nightly-git-branch-pruner/src/pruner.py

# Actually delete the merged branches (use with care)
python utils/nightly-git-branch-pruner/src/pruner.py --delete
```

## Options
- `--base <branch>` – Base branch to compare against (default: `main`).
- `--delete` – If present, the script will delete the listed branches after confirmation.
- `--protect <branch1,branch2,...>` – Comma‑separated list of branches that should never be touched even if merged (e.g., `develop,staging`).

## Testing
Run the bundled tests with:
```bash
python -m unittest utils/nightly-git-branch-pruner/tests/test_pruner.py
```
The tests use `unittest.mock` to simulate `git` commands, so they work completely offline.
