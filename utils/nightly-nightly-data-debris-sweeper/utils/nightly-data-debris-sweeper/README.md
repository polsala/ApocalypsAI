# Nightly Data Debris Sweeper

## Overview

The `nightly-data-debris-sweeper` is a whimsical yet practical utility designed to help you maintain a clean and efficient project environment. In the post-apocalyptic digital landscape, temporary files, log remnants, and cache directories can accumulate like digital rubble, slowing down your systems and consuming precious storage.

This tool allows you to define patterns for common 'debris' and either perform a dry run to see what would be cleaned or proceed with actual deletion. It's like having a diligent robot janitor for your file system, ensuring your project remains pristine and ready for the next challenge.

## Features

*   **Configurable Patterns**: Define file extensions, specific filenames, or directory names to target for cleanup.
*   **Dry Run Mode**: Safely preview all files and directories that would be affected without making any changes.
*   **Deletion Mode**: Execute the cleanup, removing identified debris.
*   **Recursive Scanning**: Scans directories recursively from a specified root path.

## Usage

```bash
python src/sweeper.py --path <directory_to_scan> [--patterns <pattern1> <pattern2> ...] [--delete]
```

### Arguments:

*   `--path <directory_to_scan>`: The root directory from which to start scanning for debris.
*   `--patterns <pattern1> <pattern2> ...`: A space-separated list of patterns to match. Patterns can be:
    *   File extensions (e.g., `.log`, `.tmp`, `.bak`)
    *   Exact filenames (e.g., `Thumbs.db`, `error.log`)
    *   Directory names (e.g., `__pycache__`, `.pytest_cache`, `node_modules`)
    *   *Note: Directory patterns will remove the entire directory and its contents.*
*   `--delete`: (Optional) If present, the utility will actually delete the identified debris. Without this flag, it performs a dry run.

### Examples:

Dry run to find common Python and temporary files in the current directory:

```bash
python src/sweeper.py --path . --patterns .log .tmp .bak __pycache__ .pytest_cache
```

Delete `node_modules` and `.DS_Store` files in a specific project directory:

```bash
python src/sweeper.py --path /path/to/my/project --patterns node_modules .DS_Store --delete
```

## Installation

This utility is self-contained and requires Python 3.11+. No external dependencies are strictly required beyond standard library modules.

To run, simply navigate to the `utils/nightly-data-debris-sweeper` directory and execute the `src/sweeper.py` script.
