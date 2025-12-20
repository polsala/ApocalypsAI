# Nightly Digital Dust Bunny Sweeper

A whimsical Bash script designed to help you maintain a tidy digital environment by identifying and optionally cleaning up old, unused files and empty directories. Think of it as a diligent little robot sweeping away the digital "dust bunnies" that accumulate over time.

## Features

*   **Identify Old Files**: Scans a specified directory for files older than a configurable number of days.
*   **Find Empty Directories**: Locates directories that contain no files or subdirectories.
*   **Whimsical Reporting**: Provides clear, friendly output about what it finds.
*   **Optional Cleaning**: Can be run in a "list only" mode or with a `--clean` flag to perform actual deletions.
*   **Safe Deletion Order**: When cleaning empty directories, it deletes them from the deepest to the shallowest to avoid issues.

## Installation

This is a standalone Bash script. No special installation is required beyond having Bash available on your system (which is standard on most Linux/macOS environments).

1.  Save the script as `nightly-dust-bunny-sweeper.sh` (or any name you prefer).
2.  Make it executable:
    ```bash
    chmod +x nightly-dust-bunny-sweeper.sh
    ```

## Usage

```bash
./nightly-dust-bunny-sweeper.sh -d <directory> [--clean] [--age <days>]
```

### Arguments

*   `-d <directory>`: **(Required)** The path to the directory you want to sweep. The script will recursively scan this directory and its subdirectories.
*   `--clean`: **(Optional)** If this flag is present, the script will proceed to delete the identified old files and empty directories. **Use with caution!** Always review the output in "list only" mode first.
*   `--age <days>`: **(Optional)** Specifies the age in days for files to be considered "ancient scrolls" (i.e., old enough to be listed/deleted). Files older than this many days will be targeted. Defaults to `30` days.

### Examples

1.  **List all digital dust bunnies in your home directory (without cleaning):**
    ```bash
    ./nightly-dust-bunny-sweeper.sh -d ~/
    ```

2.  **List files older than 60 days and empty directories in `/tmp`:**
    ```bash
    ./nightly-dust-bunny-sweeper.sh -d /tmp --age 60
    ```

3.  **Actually clean up old files and empty directories in a specific project cache:**
    ```bash
    ./nightly-dust-bunny-sweeper.sh -d /var/cache/my_app --clean
    ```

## Testing

The utility includes a self-contained test script to ensure its functionality without making actual changes to your filesystem.

1.  Navigate to the utility's directory.
2.  Run the test script:
    ```bash
    ./tests/test_nightly-dust-bunny-sweeper.sh
    ```
    This will execute a series of tests, mocking file system commands (`find`, `rm`, `rmdir`) to verify the script's logic and output without any real deletions.
