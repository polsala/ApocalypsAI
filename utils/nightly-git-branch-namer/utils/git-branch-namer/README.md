# Git Branch Namer

Utility to generate clean, conventional Git branch names from ticket IDs and titles.

## Features
- Converts any title into a URL‑friendly slug.
- Supports custom prefixes (`feature`, `bugfix`, `hotfix`, …).
- Enforces a maximum length, truncating the slug when necessary.
- Zero external dependencies – pure Python 3.11.

## Installation
```bash
# Clone the repository (or copy this folder) and ensure Python 3.11 is available.
cd utils/git-branch-namer
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (empty for now)
```

## Usage
```bash
python -m src.branch_namer \
    --ticket ABC-123 \
    --title "Add login page"
```
Will output:
```
feature/ABC-123-add-login-page
```

You can customise the prefix and maximum length:
```bash
python -m src.branch_namer \
    --ticket XYZ-9 \
    --title "Fix typo" \
    --prefix bugfix \
    --max-len 40
```

## Testing
```bash
python -m unittest discover -s tests
```
All tests should pass.
