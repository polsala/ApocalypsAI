# Nightly TODO Extractor

**Utility name:** `nightly-todo-extractor`

## Overview

`nightly-todo-extractor` walks through a given directory (recursively) and extracts all lines that look like TODO or FIXME comments from source files. It then produces a tidy Markdown report that can be committed to the repository, posted to an issue, or otherwise consumed.

## Features

- Supports common comment syntaxes (`#`, `//`, `/* */`).
- Works with any text‑based file (Python, JavaScript, Go, etc.).
- Generates a Markdown table with file paths, line numbers, and the comment text.
- Stand‑alone Python 3.11 script – no external services required.

## Installation

```bash
# From the repository root
cd utils/nightly-todo-extractor
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt  # (empty, only stdlib used)
```

## Usage

```bash
python -m src.extractor <source‑directory> <output‑markdown-file>
```

Example:

```bash
python -m src.extractor ./src ./TODO_REPORT.md
```

The script will create (or overwrite) `TODO_REPORT.md` with a table of all discovered TODO/FIXME entries.

## Testing

```bash
pytest -q
```

All tests are deterministic and run offline.
