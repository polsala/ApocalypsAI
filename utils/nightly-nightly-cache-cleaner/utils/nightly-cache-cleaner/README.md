# Nightly Cache Cleaner of Forgotten Files

## 🧹 Overview

The `nightly-cache-cleaner` is a whimsical yet practical utility designed to help you reclaim precious disk space by systematically purging old, forgotten, and temporary files from specified directories. Think of it as your digital janitor, tidying up the digital clutter that accumulates over time.

It operates based on file age and configurable include/exclude patterns, ensuring that only truly 'forgotten' files are targeted, while important data remains untouched. It supports a dry-run mode for peace of mind before any actual deletion occurs.

## ✨ Features

*   **Age-based Deletion**: Remove files older than a specified number of days.
*   **Pattern Matching**: Include or exclude files based on glob patterns (e.g., `*.log`, `temp_*`).
*   **Dry-Run Mode**: Preview which files would be deleted without actually removing them.
*   **Recursive Scan**: Traverses subdirectories to find forgotten files.
*   **Self-Contained**: No external dependencies beyond standard Python libraries.

## 🚀 Usage

```bash
python src/cleaner.py --path <directory_to_clean> --age-days <days> [--dry-run] [--include-patterns <pattern1> <pattern2> ...] [--exclude-patterns <pattern1> <pattern2> ...]
```

### Arguments:

*   `--path <directory>` (required): The root directory to start scanning for old files.
*   `--age-days <int>` (required): Files older than this many days will be considered for deletion.
*   `--dry-run`: If present, the utility will only print what *would* be deleted, without performing any actual deletions.
*   `--include-patterns <pattern1> <pattern2> ...`: One or more glob patterns (e.g., `*.tmp`, `cache/*`) to *only* consider files matching these patterns. If not provided, all files are considered (subject to `--exclude-patterns`).
*   `--exclude-patterns <pattern1> <pattern2> ...`: One or more glob patterns to *ignore* files matching these patterns. These take precedence over `--include-patterns`.

### Examples:

1.  **Dry-run to see all files older than 30 days in `/var/log/`:**
    ```bash
    python src/cleaner.py --path /var/log --age-days 30 --dry-run
    ```

2.  **Delete `.tmp` and `.bak` files older than 7 days in `~/downloads/`:**
    ```bash
    python src/cleaner.py --path ~/downloads --age-days 7 --include-patterns '*.tmp' '*.bak'
    ```

3.  **Clean up cache directories, excluding any `important.cache` files:**
    ```bash
    python src/cleaner.py --path /tmp/my_app_cache --age-days 14 --exclude-patterns 'important.cache'
    ```

## 🛠️ Development

To run tests:

```bash
python -m unittest tests/test_cleaner.py
```
