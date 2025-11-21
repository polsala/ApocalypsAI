# Nightly Repo Inspector

**Utility name:** `nightly-repo-inspector`

## Overview
`nightly-repo-inspector` walks a directory tree and produces a JSON summary containing:
- Total number of files
- Total size of all files (in bytes)
- Per‑extension breakdown of file count and cumulative size

This is handy for getting a quick snapshot of a repository’s composition without opening the project in an IDE.

## Installation
The utility is pure Python 3.11 and has no external dependencies.
```bash
# From the repository root
cd utils/nightly-repo-inspector
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (empty for now)
```

## Usage
```bash
python -m src.inspector /path/to/your/project
```
The output is printed to STDOUT as pretty‑printed JSON.

## Testing
Run the bundled tests with:
```bash
python -m unittest discover -s tests
```

## License
MIT © ApocalypsAI
