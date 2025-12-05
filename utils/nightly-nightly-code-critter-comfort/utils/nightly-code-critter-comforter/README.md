# Nightly Code Critter Comforter

The Nightly Code Critter Comforter is a whimsical-yet-useful utility designed to help you keep track of the little "critters" (TODOs, FIXMEs, BUGs, HACKs) lurking in your codebase. It scans specified directories for these common developer annotations and compiles them into a consolidated report, giving you a clear overview of your technical debt and areas needing attention.

Think of it as a friendly digital shepherd, gently nudging those forgotten tasks back into the light.

## Features

*   Scans multiple file types (Python, JavaScript, TypeScript, Go, Java, C/C++, Shell, Markdown, etc.).
*   Identifies `TODO`, `FIXME`, `BUG`, `HACK` comments (case-insensitive).
*   Generates a clear, line-by-line report of all found critters.
*   Configurable file extensions and exclusion patterns.

## Usage

To run the Comforter, navigate to the `src` directory and execute `comforter.py` with the target directory:

```bash
python src/comforter.py --path /path/to/your/project
```

### Arguments

*   `--path <directory>` (required): The root directory to start scanning from.
*   `--extensions <ext1,ext2,...>` (optional): Comma-separated list of file extensions to include (e.g., `py,js,md`). Defaults to a common set of code and documentation file extensions.
*   `--exclude <dir1,dir2,...>` (optional): Comma-separated list of directory names to exclude from the scan (e.g., `venv,node_modules`). Defaults to common exclusion patterns like `.git`, `__pycache__`, `node_modules`, etc.

## Example Report

```
Critter Report for: /path/to/your/project

---
File: /path/to/your/project/src/main.py
  Line 42: # TODO: Refactor this function for better performance.
  Line 105: # FIXME: This loop has an off-by-one error.
---
File: /path/to/your/project/docs/README.md
  Line 15: - [ ] TODO: Add more examples to the usage section.
---
File: /path/to/your/project/web/app.js
  Line 78: // HACK: This is a temporary solution until the API is stable.
---
Total Critters Found: 4 in 3 files.
```

## Development

The utility is written in Python 3.11 and is self-contained. It has no external dependencies beyond the Python standard library.

Tests are located in the `tests/` directory and can be run using `unittest` (or `pytest` if installed, though not a dependency).

```bash
python -m unittest tests/test_comforter.py
```
