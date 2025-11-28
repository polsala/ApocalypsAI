# Nightly Echo Chamber Purifier

## Overview

The Nightly Echo Chamber Purifier is a whimsical-yet-useful utility designed to combat digital redundancy. It scans specified directories for duplicate files, identifies them based on their content hash, and provides options to report or safely remove these digital echoes, thereby decluttering your storage.

In the post-apocalyptic landscape, every byte of storage is precious. This tool ensures that your data repositories are lean, efficient, and free from unnecessary clutter, making space for new discoveries or critical survival data.

## Features

*   **Content-based Duplication Detection**: Uses SHA256 hashing to accurately identify identical files, regardless of their name or timestamp.
*   **Directory Scanning**: Recursively scans one or more specified directories.
*   **Dry Run Mode**: Safely identify duplicates without making any changes.
*   **Interactive Removal**: Optionally remove duplicate files with user confirmation.
*   **Report Generation**: Outputs a clear list of all identified duplicate groups.

## Installation

This utility is self-contained and requires Python 3.6+.

1.  Navigate to the utility's directory:
    ```bash
    cd utils/nightly-echo-chamber-purifier
    ```
2.  The `src/purifier.py` script is directly runnable.

## Usage

```bash
python src/purifier.py --help
```

### Basic Scan (Dry Run)

To find duplicates in a directory without removing them:

```bash
python src/purifier.py --path /path/to/your/directory
```

### Scan Multiple Directories

```bash
python src/purifier.py --path /path/to/dir1 /path/to/dir2
```

### Remove Duplicates (Interactive)

To remove duplicates, use the `--remove` flag. The script will prompt you before deleting each duplicate file.

```bash
python src/purifier.py --path /path/to/your/directory --remove
```

### Exclude Directories

To exclude specific subdirectories from the scan (e.g., `.git`, `node_modules`):

```bash
python src/purifier.py --path /path/to/your/directory --exclude .git node_modules
```

### Minimum File Size

To ignore very small files (e.g., empty files or tiny config files) that might be duplicates but not worth cleaning:

```bash
python src/purifier.py --path /path/to/your/directory --min-size 1024 # Ignore files smaller than 1KB
```

## Development

### Running Tests

```bash
python -m unittest tests/test_purifier.py
```
