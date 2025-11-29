# Nightly Cosmic Cache Cleaner

## Overview

The Nightly Cosmic Cache Cleaner is a whimsical-yet-powerful utility designed to help you reclaim precious disk space by tidying up the digital detritus of your development projects. It scours specified directories for common cache folders (like `__pycache__`, `node_modules`, `.pytest_cache`, etc.) and offers to remove them, or simply report what it *would* remove in a dry run. Think of it as a tiny, diligent cosmic janitor for your file system!

## Features

*   **Pattern-based Cleaning**: Define a list of directory names to target for cleanup.
*   **Recursive Scan**: Traverses directories from a specified root to find all matching caches.
*   **Dry Run Mode**: Preview what would be deleted without making any changes.
*   **Space Saving Report**: Provides a summary of the disk space reclaimed.
*   **Self-contained**: No external dependencies beyond standard Python libraries.

## Usage

```bash
python src/cleaner.py [OPTIONS]
```

### Options

*   `--path <directory>`: The root directory to start scanning from. Defaults to the current working directory (`.`).
*   `--patterns <pattern1> <pattern2> ...`: A space-separated list of directory names to clean. Common examples include `__pycache__`, `node_modules`, `.pytest_cache`, `.mypy_cache`, `dist`, `build`. Defaults to `__pycache__ node_modules .pytest_cache .mypy_cache`.
*   `--dry-run`: Perform a dry run. The utility will list all directories it *would* delete and report the potential space savings, but will not actually remove anything.
*   `--verbose`: Print detailed information about each directory found.

### Examples

1.  **Dry run in the current directory for default patterns:**
    ```bash
    python src/cleaner.py --dry-run
    ```

2.  **Clean `node_modules` and `dist` folders in a specific project directory:**
    ```bash
    python src/cleaner.py --path /path/to/my/project --patterns node_modules dist
    ```

3.  **Verbose dry run for all default patterns:**
    ```bash
    python src/cleaner.py --dry-run --verbose
    ```

## Installation

This utility is self-contained. Simply place the `nightly-cosmic-cache-cleaner` folder within your `utils/` directory.

## Development

To run tests:

```bash
python -m unittest tests/test_cleaner.py
```
