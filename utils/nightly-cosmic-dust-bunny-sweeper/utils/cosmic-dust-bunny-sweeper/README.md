# Cosmic Dust Bunny Sweeper

## Overview
The `cosmic-dust-bunny-sweeper` is a whimsical yet practical utility designed to help you maintain a clean and efficient filesystem. It scans specified directories for "digital dust bunnies" – old, forgotten files and empty directories – and provides options to list or remove them. Keep your digital space tidy, even when the physical world is in disarray!

## Features
-   **Age-based File Cleanup**: Identify and remove files older than a specified number of days.
-   **Empty Directory Removal**: Automatically detect and remove empty directories.
-   **Dry Run Mode**: Preview what would be deleted before making any changes.
-   **Recursive Scanning**: Scans directories and all their subdirectories.

## Usage

```bash
python src/sweeper.py --path /path/to/scan --age 30 --mode list
python src/sweeper.py --path /path/to/scan --age 7 --mode delete --confirm
python src/sweeper.py --path /path/to/scan --mode list-empty-dirs
python src/sweeper.py --path /path/to/scan --mode delete-empty-dirs --confirm
```

### Arguments:
-   `--path <directory>`: The root directory to start scanning from. (Required)
-   `--age <days>`: Files older than this many days will be considered for cleanup. (Default: 30)
-   `--mode <list|delete|list-empty-dirs|delete-empty-dirs>`:
    -   `list`: Lists files older than `--age`.
    -   `delete`: Deletes files older than `--age`. Requires `--confirm`.
    -   `list-empty-dirs`: Lists empty directories.
    -   `delete-empty-dirs`: Deletes empty directories. Requires `--confirm`.
-   `--confirm`: Required for `delete` and `delete-empty-dirs` modes to prevent accidental data loss.

## Examples

**List files older than 60 days in your downloads folder:**
```bash
python src/sweeper.py --path ~/Downloads --age 60 --mode list
```

**Delete files older than 7 days in a temporary directory (use with caution!):**
```bash
python src/sweeper.py --path /tmp/my_app_cache --age 7 --mode delete --confirm
```

**List all empty directories in your project folder:**
```bash
python src/sweeper.py --path ~/Projects --mode list-empty-dirs
```

**Delete all empty directories in your logs folder:**
```bash
python src/sweeper.py --path /var/log/my_app --mode delete-empty-dirs --confirm
```

## Development
To run tests:
```bash
python -m unittest tests/test_sweeper.py
```
