# Digital Dust Bunny Sweeper

## Overview

In the digital wasteland, old, forgotten files accumulate like dust bunnies under a derelict server rack. The `digital-dust-bunny-sweeper` is a whimsical-yet-useful utility designed to help you reclaim precious disk space by identifying and optionally removing these digital 'dust bunnies' – files that haven't been touched in a specified period.

Keep your digital sanctuary clean and efficient, even when the world outside is anything but.

## Features

*   **Directory Scanning**: Recursively scans a specified directory for files.
*   **Age-Based Filtering**: Identifies files older than a user-defined number of days.
*   **Dry Run Mode**: Preview which files would be deleted without actually removing them.
*   **Interactive Deletion**: Prompts for confirmation before deleting files.
*   **Force Deletion**: Delete all identified files without prompting (use with extreme caution).
*   **Simple CLI**: Easy to use from the command line.

## Installation

This utility is self-contained. Simply navigate to the `utils/digital-dust-bunny-sweeper/src` directory.

## Usage

```bash
python src/sweeper.py --directory /path/to/scan --age 90
```

**Arguments:**

*   `--directory <path>` (required): The root directory to scan for old files.
*   `--age <days>` (required): The minimum age in days for a file to be considered a 'dust bunny'.
*   `--dry-run` (optional): If present, the utility will only list files that *would* be deleted, without actually deleting them. This is the default behavior if no other deletion flag is used.
*   `--confirm-delete` (optional): If present, the utility will prompt for confirmation before deleting each file. This flag is ignored if `--force-delete` is also present.
*   `--force-delete` (optional): If present, the utility will delete all identified files without prompting. **Use with extreme caution!** This overrides `--dry-run` and `--confirm-delete`.

**Examples:**

1.  **List files older than 30 days in your downloads folder (dry run):**
    ```bash
    python src/sweeper.py --directory ~/Downloads --age 30 --dry-run
    ```

2.  **Interactively delete files older than 180 days in a project archive:**
    ```bash
    python src/sweeper.py --directory /var/archive/old_projects --age 180 --confirm-delete
    ```

3.  **Force delete all files older than 7 days in a temporary directory (DANGEROUS!):**
    ```bash
    python src/sweeper.py --directory /tmp/cache --age 7 --force-delete
    ```

## Development

To run tests:

```bash
python -m unittest tests/test_sweeper.py
```
