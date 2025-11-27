# Nightly Temporal Tangle Tracker

The Nightly Temporal Tangle Tracker is a whimsical-yet-useful utility designed to help you unearth and manage the forgotten "tangles" of technical debt lurking in your codebase. It scans specified directories for common markers like `TODO`, `FIXME`, and `HACK`, compiling them into a clear, categorized report.

Don't let your codebase become a temporal tangle of forgotten intentions!

## Features

*   **Keyword Scanning**: Configurable keywords (default: `TODO`, `FIXME`, `HACK`).
*   **Directory Traversal**: Recursively scans files within a specified directory.
*   **Categorized Reporting**: Groups findings by keyword and file, providing line numbers and the full comment.
*   **Markdown Output**: Generates a human-readable Markdown report.

## Installation

This utility is self-contained and written in Python 3.11+. No external dependencies are required beyond the standard library.

1.  Navigate to the `utils/nightly-temporal-tangle-tracker` directory.
2.  Ensure you have Python 3.11 or newer installed.

## Usage

Run the `tracker.py` script from the command line:

```bash
python src/tracker.py --path <directory_to_scan> [--keywords <kw1> <kw2> ...] [--output <output_file.md>]
```

### Arguments:

*   `--path <directory_to_scan>` (required): The root directory to start scanning from.
*   `--keywords <kw1> <kw2> ...` (optional): A space-separated list of keywords to search for. Defaults to `TODO`, `FIXME`, `HACK`.
*   `--output <output_file.md>` (optional): The path to save the Markdown report. If not provided, the report will be printed to stdout.
*   `--exclude-dirs <dir1> <dir2> ...` (optional): A space-separated list of directory names to exclude from scanning (e.g., `.git`, `node_modules`). Defaults to common exclusion patterns.

### Example:

```bash
# Scan the current directory for default keywords and print to console
python src/tracker.py --path .

# Scan a specific project directory for custom keywords and save to a file
python src/tracker.py --path /path/to/my/project --keywords TODO BUG --output project_tangles.md

# Scan a directory, excluding 'build' and 'dist' folders
python src/tracker.py --path . --exclude-dirs build dist
```

## How it Works

The script walks through the specified directory, reading each file line by line. It uses regular expressions to efficiently find occurrences of the defined keywords, extracting the full comment. Binary files and files within common ignored directories (like `.git`, `node_modules`, `__pycache__`) are automatically skipped to prevent errors and reduce noise.

## Development & Testing

To run the tests, navigate to the utility's root directory and ensure `pytest` is installed (`pip install pytest`), then execute:

```bash
python -m pytest tests/
```
