# Nightly Echo Chamber Purifier

## Overview

The Nightly Echo Chamber Purifier is a utility designed to help maintain a clean and efficient repository by identifying and managing duplicate files. It scans a specified directory, calculates SHA256 hashes for all files, and reports any files that have identical content. Optionally, it can delete the duplicate copies, keeping only one original.

This tool is particularly useful for cleaning up build artifacts, temporary files, or accidental copies that accumulate over time, ensuring that your project's 'echo chamber' of redundant data is purified.

## Usage

```bash
python src/purifier.py <directory_to_scan> [--delete] [--dry-run]
```

### Arguments:

*   `<directory_to_scan>`: The root directory to start scanning for duplicate files.
*   `--delete`: (Optional) If provided, the utility will delete all but one instance of each set of duplicate files. **Use with caution!** By default, it only reports.
*   `--dry-run`: (Optional) If provided, the utility will only report what *would* be deleted without making any changes. This is the default behavior if `--delete` is not specified.

## Examples

1.  **Find duplicates in the current directory (dry run):**

    ```bash
    python src/purifier.py .
    ```

2.  **Find duplicates in a 'build' directory and delete them:**

    ```bash
    python src/purifier.py ./build --delete
    ```

3.  **Find duplicates in 'temp' directory (explicit dry run):**

    ```bash
    python src/purifier.py ./temp --dry-run
    ```

## How it Works

The purifier performs the following steps:

1.  It walks through the specified directory and all its subdirectories.
2.  For each file encountered, it calculates a SHA256 hash of its content.
3.  It stores file paths grouped by their hash.
4.  After scanning all files, it identifies groups with more than one file (these are the duplicates).
5.  It then reports these duplicates. If `--delete` is specified and `--dry-run` is not, it removes all but the first encountered file in each duplicate group.

## Requirements

*   Python 3.6+

## Development

To run tests:

```bash
python -m unittest tests/test_purifier.py
```
