# Nightly Cosmic Dust Collector

## Overview

The Nightly Cosmic Dust Collector is a whimsical-yet-useful utility designed to help keep your repository clean and tidy. It scans specified directories for "cosmic dust" – old, forgotten, or temporary files that accumulate over time. By identifying these files based on their age and configurable patterns, it helps you maintain a lean and efficient project space, preventing digital clutter from obscuring your stellar work.

## Features

*   **Age-based Filtering**: Identify files older than a specified number of days.
*   **Pattern Matching**: Target specific types of files (e.g., logs, temporary files, backups) using glob patterns.
*   **Dry Run (Default)**: Safely list files that match the criteria without performing any destructive actions.
*   **Self-contained**: No external dependencies beyond standard Python libraries.

## Usage

```bash
python src/dust_collector.py --path <directory_to_scan> [--age <days>] [--patterns <pattern1> <pattern2> ...] [--exclude-dirs <dir1> <dir2> ...]
```

### Arguments

*   `--path <directory_to_scan>`: **Required**. The root directory to start scanning for dust.
*   `--age <days>`: Optional. The minimum age in days for a file to be considered "dust". Defaults to `30` days.
*   `--patterns <pattern1> <pattern2> ...`: Optional. One or more glob patterns (e.g., `*.log`, `tmp_*`, `*.bak`) to match against filenames. If no patterns are provided, all files older than the specified age will be considered.
*   `--exclude-dirs <dir1> <dir2> ...`: Optional. One or more directory names to exclude from the scan (e.g., `.git`, `node_modules`).

### Examples

1.  **Find all files older than 60 days in the current directory:**
    ```bash
    python src/dust_collector.py --path . --age 60
    ```

2.  **Find all `.log` and `.tmp` files older than 7 days in the `logs/` directory:**
    ```bash
    python src/dust_collector.py --path logs/ --age 7 --patterns "*.log" "*.tmp"
    ```

3.  **Find all old files, excluding `.git` and `venv` directories:**
    ```bash
    python src/dust_collector.py --path . --age 90 --exclude-dirs ".git" "venv"
    ```

## Output

The utility will print a list of files identified as "cosmic dust", along with their size and last modified date.

```
Cosmic Dust Report for /path/to/scan:

- /path/to/scan/old_log.log (1.2 KB, Last Modified: 2023-01-15)
- /path/to/scan/temp/temp_file.tmp (500 B, Last Modified: 2023-02-01)
- /path/to/scan/backup/data.bak (10.5 MB, Last Modified: 2022-12-20)

Total dust found: 3 files, 10.5 MB
```

## Development

This utility is written in Python 3.11 and uses standard library modules only.
Tests are located in `tests/test_dust_collector.py` and can be run using `pytest` or `python -m unittest`.
