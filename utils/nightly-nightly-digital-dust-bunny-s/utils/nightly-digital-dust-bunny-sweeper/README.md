# Nightly Digital Dust Bunny Sweeper

## Overview

The `nightly-digital-dust-bunny-sweeper` is a whimsical-yet-useful utility designed to help you reclaim precious disk space by tidying up your project directories. It identifies and offers to remove common 'dust bunnies' – temporary files, cache directories, and old, forgotten files – that accumulate over time.

## Features

*   **Targeted Cleanup**: Scans for specific patterns like `__pycache__` directories and `.DS_Store` files.
*   **Age-Based Deletion**: Can identify and remove files older than a specified number of days.
*   **Dry Run Mode**: Safely preview what would be deleted before making any changes.
*   **Recursive Scan**: Traverses directories to find hidden clutter.

## Usage

```bash
python src/dust_bunny_sweeper.py --path <directory_to_scan> [OPTIONS]
```

### Arguments

*   `--path <directory>`: The root directory to start scanning from. (Required)

### Options

*   `--delete`: Perform actual deletion. If omitted, the utility runs in dry-run mode (list only).
*   `--patterns <pattern1> <pattern2> ...`: A space-separated list of file/directory names to target (e.g., `__pycache__ .DS_Store`). Defaults to `__pycache__ .DS_Store`.
*   `--max-age-days <days>`: Delete files older than this many days. Applies to all files, not just pattern-matched ones. (e.g., `30` for files older than 30 days).
*   `--verbose`: Print detailed information about files found and actions taken.

### Examples

1.  **Dry run: List all `__pycache__` and `.DS_Store` files in the current directory and its subdirectories:**
    ```bash
    python src/dust_bunny_sweeper.py --path .
    ```

2.  **Delete `__pycache__` and `.DS_Store` files in a specific project directory:**
    ```bash
    python src/dust_bunny_sweeper.py --path /path/to/my/project --delete
    ```

3.  **Delete all files older than 90 days in your downloads folder (dry run):**
    ```bash
    python src/dust_bunny_sweeper.py --path ~/Downloads --max-age-days 90
    ```

4.  **Delete specific log files (`*.log`) older than 7 days in a logs directory:**
    ```bash
    python src/dust_bunny_sweeper.py --path /var/log --patterns "*.log" --max-age-days 7 --delete
    ```

## Installation

This utility is self-contained and requires Python 3.6+.

1.  Navigate to the utility's directory:
    ```bash
    cd utils/nightly-digital-dust-bunny-sweeper
    ```
2.  Run directly:
    ```bash
    python src/dust_bunny_sweeper.py --help
    ```
