# Nightly Echo Chamber Purifier

## Purpose

The Nightly Echo Chamber Purifier is a whimsical yet highly practical utility designed to detect and optionally remove duplicate files within specified directories. In the digital age, files can multiply, creating "echo chambers" of redundant data that consume valuable storage space and clutter your system. This tool helps you identify and clean up these digital echoes, ensuring your file system is lean and efficient.

## Features

*   **Duplicate Detection**: Scans one or more directories to find files with identical content.
*   **Content-Based Hashing**: Uses MD5 hashing to ensure accurate content comparison, not just file names or sizes.
*   **Dry Run Mode**: Preview which files would be removed without actually deleting anything.
*   **Safe Removal**: Optionally remove duplicate files, keeping only the first encountered instance.
*   **Recursive Scan**: Traverses subdirectories to find duplicates everywhere.

## Usage

### Command Line Interface

```bash
python src/purifier.py <directory_path_1> [directory_path_2 ...] [--remove] [--verbose]
```

*   `<directory_path>`: One or more paths to directories to scan for duplicates.
*   `--remove`: (Optional) If specified, duplicate files will be deleted. By default, it performs a dry run and only lists them.
*   `--verbose`: (Optional) If specified, prints more detailed information during the scan.

### Examples

1.  **Find duplicates in a single directory (dry run):**
    ```bash
    python src/purifier.py /path/to/my/documents
    ```

2.  **Find duplicates across multiple directories and remove them:**
    ```bash
    python src/purifier.py /path/to/photos /path/to/downloads --remove
    ```

3.  **Find duplicates with verbose output (dry run):**
    ```bash
    python src/purifier.py /path/to/project --verbose
    ```

## How it Works

The purifier calculates an MD5 hash for the content of each file it encounters. Files with identical MD5 hashes are considered duplicates. For each set of duplicates, the first file encountered is considered the "original," and subsequent files with the same hash are marked as duplicates. In `--remove` mode, these marked duplicates are then deleted.

## Installation

This utility is self-contained. Simply navigate to the `utils/nightly-echo-chamber-purifier/` directory and run the `purifier.py` script. No special installation steps or external dependencies are required beyond Python 3.6+.

## Testing

To run the automated tests, navigate to the utility's root directory and execute:

```bash
python -m unittest tests/test_purifier.py
```
