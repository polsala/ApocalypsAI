# Nightly Temporal Tear Tidy-Upper

## Overview

The `nightly-temporal-tear-tidy-upper` is a whimsical yet practical command-line utility designed to help you maintain a pristine project wasteland. It scans a specified directory for files older than a certain age and for empty directories, offering a dry-run mode before any actual deletion.

Keep your digital ruins organized and free from temporal detritus!

## Features

*   **Identify Old Files**: Find files that haven't been modified in a specified number of days.
*   **Identify Empty Directories**: Locate directories that contain no files or subdirectories.
*   **Dry Run Mode**: Preview what would be deleted without making any changes. This is the default behavior if `--delete` is not specified.
*   **Deletion Mode**: Safely remove identified old files and empty directories. This overrides `--dry-run` if both are present.

## Usage

```bash
python src/tidy_upper.py --path <directory_to_clean> [--age <days>] [--dry-run] [--delete]
```

### Arguments:

*   `--path <directory_to_clean>`: **Required**. The root directory to scan for old files and empty directories.
*   `--age <days>`: Optional. The minimum age in days for a file to be considered 'old'. Defaults to 30 days. Files older than this will be flagged.
*   `--dry-run`: Optional. If present, the utility will only list files and directories that *would* be deleted, without actually deleting them. This is the default behavior if `--delete` is not specified. If `--delete` is also present, `--delete` takes precedence.
*   `--delete`: Optional. If present, the utility will proceed with deleting the identified old files and empty directories. **Use with caution!** This flag overrides `--dry-run`.

### Examples:

1.  **Dry run to see files older than 60 days in the current directory:**
    ```bash
    python src/tidy_upper.py --path . --age 60 --dry-run
    ```

2.  **Delete files older than 7 days and empty directories in a specific project folder:**
    ```bash
    python src/tidy_upper.py --path /path/to/my/project --age 7 --delete
    ```

3.  **Just list empty directories in a folder (default age 30, dry-run default):**
    ```bash
    python src/tidy_upper.py --path /path/to/another/project
    ```

## Development & Testing

To run the tests for this utility:

```bash
python -m unittest tests/test_tidy_upper.py
```
