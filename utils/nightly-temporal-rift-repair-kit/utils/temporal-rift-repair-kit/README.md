# Temporal Rift Repair Kit

## Overview

The "Temporal Rift Repair Kit" is a whimsical-yet-useful utility designed to help you reclaim precious disk space by identifying and optionally deleting old or excessively large temporary files across specified directories. Think of it as patching up the "temporal rifts" that accumulate on your filesystem, preventing them from consuming your digital reality.

It's particularly useful for development environments, build caches, or any directory prone to accumulating transient data.

## Features

*   **Directory Scanning**: Recursively scans one or more specified directories.
*   **Age-Based Filtering**: Identifies files older than a configurable number of days.
*   **Size-Based Filtering**: Identifies files larger than a configurable minimum size.
*   **Dry Run Mode**: Preview which files would be deleted without actually removing them.
*   **Interactive Deletion**: Prompts for confirmation before deleting files (optional).

## Installation

This utility is self-contained and written in Python 3.11+. No external dependencies are required beyond the standard library.

To use it, simply navigate to the `utils/temporal-rift-repair-kit/src` directory and run the `rift_repair.py` script.

## Usage

```bash
python3 rift_repair.py --help
```

### Examples

1.  **Scan a single directory for files older than 30 days and larger than 10MB (dry run):**
    ```bash
    python3 rift_repair.py --path /var/tmp --max-age 30 --min-size 10240 --dry-run
    ```
    (Note: `min-size` is in KB, so 10MB = 10240KB)

2.  **Scan multiple directories, delete files older than 7 days, regardless of size (interactive):**
    ```bash
    python3 rift_repair.py --path /tmp /var/cache/apt --max-age 7 --confirm
    ```

3.  **Scan a directory for files larger than 500MB, no age limit (dry run):**
    ```bash
    python3 rift_repair.py --path ~/Downloads --min-size 512000 --dry-run
    ```

## Command-Line Arguments

*   `--path <directory> [<directory> ...]`: **Required**. One or more paths to directories to scan.
*   `--max-age <days>`: Files older than this many days will be considered for deletion. Default: `30`.
*   `--min-size <KB>`: Files larger than this many kilobytes will be considered for deletion. Default: `0` (no minimum size).
*   `--dry-run`: If set, the utility will only report files that *would* be deleted, without actually deleting them.
*   `--confirm`: If set, the utility will prompt for confirmation before deleting each file or group of files. If not set, it will delete without prompting (unless `--dry-run` is also set).

## Development & Testing

To run the tests, navigate to the `utils/temporal-rift-repair-kit` directory and execute:

```bash
python3 -m unittest tests/test_rift_repair.py
```
