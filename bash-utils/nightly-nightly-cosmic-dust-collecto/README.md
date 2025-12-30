# Nightly Cosmic Dust Collector

A whimsical Bash script designed to help you keep your digital cosmos tidy by sweeping away "cosmic dust" – old temporary files, logs, and empty directories that accumulate over time. Think of it as a celestial janitor for your file system!

## ✨ Features

*   **Whimsical Reporting**: Get a summary of the "cosmic dust" (disk space) collected.
*   **Configurable Paths**: Easily define which directories to scan for old files and empty voids.
*   **Age-Based Cleanup**: Only files older than a specified number of days are considered "dust."
*   **Dry Run Mode**: Preview what would be deleted without actually removing anything.
*   **Verbose Output**: See detailed information about each file and directory processed.
*   **Safe Defaults**: Designed to be run safely, but always review paths before execution.

## 🚀 Usage

1.  **Make it executable**:
    ```bash
    chmod +x src/cosmic_dust_collector.sh
    ```

2.  **Run a dry-run (highly recommended first!)**:
    This will show you what files *would* be removed without actually deleting them.
    ```bash
    ./src/cosmic_dust_collector.sh --dry-run
    # Or short form:
    ./src/cosmic_dust_collector.sh -d
    ```

3.  **Run with verbose output (dry-run)**:
    ```bash
    ./src/cosmic_dust_collector.sh -d -v
    ```

4.  **Perform actual cleanup**:
    **_Use with caution! Ensure you understand what will be deleted._**
    ```bash
    ./src/cosmic_dust_collector.sh
    ```

5.  **View help**:
    ```bash
    ./src/cosmic_dust_collector.sh --help
    ```

## ⚙️ Configuration

The script's configuration is embedded directly within `src/cosmic_dust_collector.sh`. You can easily modify the following variables:

*   `CLEANUP_PATHS`: An array of directories to scan.
    ```bash
    declare -a CLEANUP_PATHS=(
        "/tmp"
        "/var/log"
        "${HOME}/.cache"
        # Add your custom paths here, e.g., "/opt/my_app/temp_data"
    )
    ```
    **Important**: Be cautious when adding paths, especially system-critical ones. Always test with `--dry-run` first.

*   `OLD_FILES_DAYS`: The minimum age (in days) for a file to be considered "cosmic dust" and eligible for deletion.
    ```bash
    OLD_FILES_DAYS=7 # Files older than 7 days
    ```

## 🧪 Testing

The utility includes a self-contained test suite.

1.  **Make the test script executable**:
    ```bash
    chmod +x tests/test_collector.sh
    ```

2.  **Run the tests**:
    ```bash
    ./tests/test_collector.sh
    ```
    The tests use mocks for `find`, `du`, `rm`, `rmdir`, and `date` to ensure determinism and prevent actual file system modifications during testing.
