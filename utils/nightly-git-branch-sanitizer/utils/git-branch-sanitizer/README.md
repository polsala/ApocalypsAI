# Git Branch Sanitizer

Utility to normalise Git branch names into a safe, kebab‑case format.

## Features
- Strips leading/trailing whitespace
- Replaces spaces and underscores with hyphens
- Removes characters illegal in Git refs (except `.` and `-`)
- Collapses multiple hyphens
- Lower‑cases the result
- Guarantees the name does not start or end with a hyphen

## Installation
```bash
# From the repository root
cd utils/git-branch-sanitizer
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (no external deps needed)
```

## Usage
```bash
python -m src.sanitize_branch "Feature/Add New_Stuff!"
# => feature-add-new-stuff
```

## Testing
```bash
python -m unittest discover -s tests
```
