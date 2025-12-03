# Nightly Cosmic Dust Collector

## Overview

The `nightly-cosmic-dust-collector` is a whimsical yet practical utility designed to help you maintain a tidy repository by identifying and managing 'cosmic dust' – small, forgotten, or empty files that accumulate over time. Think of it as a digital broom for your file system, sweeping away the tiny particles that contribute to clutter.

## Features

*   **Scan Directories**: Recursively scans a specified directory for files meeting certain criteria (e.g., size threshold, emptiness).
*   **Identify Dust**: Flags files as 'cosmic dust' if they are smaller than a configurable size or are completely empty.
*   **List Mode**: Simply lists the identified dust files without making any changes.
*   **Archive Mode**: Moves identified dust files into a dedicated `.dust_archive` subdirectory within the scanned path, preserving them for later review.
*   **Delete Mode**: Permanently removes identified dust files (use with caution and dry-run first!).
*   **Dry Run**: Preview actions before committing to them.

## Installation

This utility is self-contained and requires Python 3.8+.

1.  Navigate to the utility's directory:
    ```bash
    cd utils/nightly-cosmic-dust-collector
    ```
2.  The utility has no external dependencies beyond standard Python libraries.

## Usage

Run the `dust_collector.py` script from its directory or by specifying its full path.

```bash
python src/dust_collector.py --help
```

**Examples:**

1.  **List all files smaller than 100 bytes in the current directory (dry run):**
    ```bash
    python src/dust_collector.py . --max-size 100 --dry-run --mode list
    ```

2.  **Archive empty files in a specific project folder:**
    ```bash
    python src/dust_collector.py /path/to/my/project --empty-only --mode archive
    ```

3.  **Delete files smaller than 50 bytes in a temporary directory (after reviewing with dry-run):**
    ```bash
    python src/dust_collector.py /tmp/old_logs --max-size 50 --mode delete
    ```

### Command Line Arguments

*   `PATH`: The directory to scan (required).
*   `--mode {list,archive,delete}`: Operation mode. `list` is default if not specified.
*   `--max-size SIZE_BYTES`: Maximum file size in bytes to consider as dust. Default: 1024 bytes (1KB).
*   `--empty-only`: Only consider empty files as dust, ignoring `--max-size`.
*   `--dry-run`: Show what would be done without making any changes.
*   `--archive-dir NAME`: Name of the subdirectory to move archived files into. Default: `.dust_archive`.

## Development & Testing

To run the tests, navigate to the utility's root directory and use `python -m unittest`:

```bash
python -m unittest tests/test_dust_collector.py
```
