# Nightly Digital Dust-Buster

## Overview

The Nightly Digital Dust-Buster is a whimsical-yet-useful utility designed to help you maintain a clean and efficient digital workspace in the post-apocalyptic landscape. It scans specified directories for digital "dust" and "debris" – specifically, broken symbolic links and empty directories – and provides options to list or remove them. Keep your system tidy, just like a good scavenger keeps their camp!

## Features

*   **Broken Symlink Detection**: Identifies symbolic links that point to non-existent files or directories.
*   **Empty Directory Cleanup**: Finds and lists directories that contain no files or subdirectories.
*   **Safe Listing Mode**: Preview what would be removed before making any changes.
*   **Deletion Mode**: Automatically remove identified broken symlinks and empty directories.

## Installation

This utility is self-contained and written in Python 3.11+. No external dependencies are required beyond the standard library.

1.  Navigate to the `utils/nightly-digital-dust-buster/` directory.
2.  Run directly using Python.

## Usage

```bash
python src/dust_buster.py --path <directory_to_scan> [--delete]
```

### Arguments

*   `--path <directory_to_scan>`: **Required**. The root directory from which to start scanning. The scan will be recursive.
*   `--delete`: **Optional**. If provided, the utility will *delete* the identified broken symbolic links and empty directories. **Use with caution!** If omitted, the utility will only list the findings.

### Examples

1.  **List all broken symlinks and empty directories in your home directory (without deleting):**
    ```bash
    python src/dust_buster.py --path ~/ 
    ```

2.  **Delete all broken symlinks and empty directories in a specific project folder:**
    ```bash
    python src/dust_buster.py --path /path/to/my/project --delete
    ```

## Development

To run tests:

```bash
python -m unittest tests/test_dust_buster.py
```
