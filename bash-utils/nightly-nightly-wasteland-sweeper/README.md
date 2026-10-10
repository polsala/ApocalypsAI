# Nightly Wasteland Sweeper

A whimsical-yet-useful bash script to help you clean up your digital "wasteland" by identifying and optionally removing old files and empty directories in specified paths. Think of it as a post-apocalyptic cleanup crew for your file system, ensuring only the truly necessary (or recently touched) data survives.

## Features

*   **Old File Detection**: Scans for files older than a specified number of days.
*   **Empty Directory Cleanup**: Identifies and lists empty directories.
*   **Dry Run Mode**: Preview what would be deleted without making any changes.
*   **Interactive Confirmation**: Prompts for confirmation before performing actual deletions.
*   **Recursive Cleanup**: Works on the specified path and all its subdirectories.

## Usage

```bash
./src/wasteland_sweeper.sh <path> [age_in_days] [--dry-run]
```

### Arguments

*   `<path>`: The root directory to start the sweep from. This directory will be scanned recursively.
*   `[age_in_days]`: (Optional) An integer specifying the age threshold in days. Files older than this many days will be targeted for removal. Defaults to `7` days if not provided.
*   `--dry-run`: (Optional) If present, the script will only list the files and directories that *would* be removed, without actually deleting anything. This is highly recommended for a first run!

### Examples

1.  **Dry run to see old files (older than 7 days) and empty directories in your home folder:**
    ```bash
    ./src/wasteland_sweeper.sh ~/ --dry-run
    ```

2.  **Dry run to see old files (older than 30 days) and empty directories in a specific project folder:**
    ```bash
    ./src/wasteland_sweeper.sh /var/log/old_archives 30 --dry-run
    ```

3.  **Perform a live cleanup of files older than 14 days and empty directories in a temporary folder (will prompt for confirmation):**
    ```bash
    ./src/wasteland_sweeper.sh /tmp/my_temp_data 14
    ```

4.  **Perform a live cleanup with default age (7 days) in a downloads folder (will prompt for confirmation):**
    ```bash
    ./src/wasteland_sweeper.sh ~/Downloads
    ```

## Installation

This is a standalone bash script. Simply ensure it's executable:

```bash
chmod +x ./src/wasteland_sweeper.sh
```

## Testing

To run the tests, navigate to the utility's root directory and execute the test script:

```bash
./tests/test_wasteland_sweeper.sh
```

The tests use mocks for `find`, `rm`, and `read` to ensure determinism and avoid actual file system modifications during testing.
