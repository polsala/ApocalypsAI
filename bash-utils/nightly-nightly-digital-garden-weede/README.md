# Nightly Digital Garden Weeder

The `nightly-digital-garden-weeder` is a whimsical-yet-useful utility designed to keep your digital filesystem tidy by automatically pruning old, temporary, and cached files. Think of it as a diligent gardener for your system, weeding out the digital clutter that accumulates over time.

## 🪴 Features

*   **Automated Pruning**: Cleans up files older than a specified retention period.
*   **Configurable Retention**: Easily set how many days files should be kept.
*   **Targeted Directories**: Specify which directories to weed, with sensible defaults.
*   **Dry Run Mode**: Simulate the cleanup process to see what would be deleted without making any changes.
*   **Whimsical Reporting**: Provides a "Digital Garden Weeder Report" summary.

## 🚀 Usage

The `weeder.sh` script can be run directly from your terminal.

```bash
./src/weeder.sh [OPTIONS]
```

### Options:

*   `--dry-run`: Simulate the cleanup without actually deleting files. This is highly recommended for your first run!
*   `--days <N>`: Retain files for `N` days. Files older than `N` days will be targeted for deletion. Default is `7` days. `N` must be a positive integer.
*   `--dirs <dir1> <dir2> ...`: Specify one or more directories to clean. If not provided, the script defaults to common temporary and cache locations like `/tmp`, `/var/tmp`, `$HOME/.cache`, and `$HOME/.local/share/Trash/files`.
*   `--help`: Display the usage information and exit.

### Examples:

1.  **Perform a dry run with default settings (7 days retention, default directories):**
    ```bash
    ./src/weeder.sh --dry-run
    ```

2.  **Clean files older than 30 days in your home cache directory:**
    ```bash
    ./src/weeder.sh --days 30 --dirs "$HOME/.cache"
    ```

3.  **Perform a dry run on multiple specific directories, retaining files for 14 days:**
    ```bash
    ./src/weeder.sh --dry-run --days 14 --dirs "/var/log/old" "/opt/app/temp"
    ```

4.  **Live run (DANGER: files will be deleted!) with default settings:**
    ```bash
    ./src/weeder.sh
    ```
    *(Always use `--dry-run` first to understand the impact!)*

## 🛠️ Installation

This utility is a standalone Bash script. No special installation is required beyond ensuring you have Bash available (which is standard on most Linux/macOS systems).

1.  Clone the `polsala/ApocalypsAI` repository (if you haven't already).
2.  Navigate to the `bash-utils/nightly-digital-garden-weeder` directory.
3.  Make the script executable:
    ```bash
    chmod +x src/weeder.sh
    ```

## 🧪 Testing

To run the automated tests for this utility:

```bash
./tests/test_weeder.sh
```

The tests create temporary files with specific modification times in a dedicated test directory, then run the `weeder.sh` script in both dry-run and live modes to verify its behavior. All temporary files are cleaned up automatically after the tests complete.

## ⚠️ Important Considerations

*   **Permissions**: The script runs with the permissions of the user executing it. Ensure it has the necessary permissions to read and delete files in the target directories.
*   **Root Privileges**: For cleaning system-wide temporary directories (like `/tmp` or `/var/tmp` if they contain files owned by other users), you might need to run the script with `sudo`. Exercise extreme caution when running any deletion script with `sudo`.
*   **Backup**: Always have backups of important data. While this tool targets temporary files, misconfiguration or unexpected behavior could lead to data loss. Use `--dry-run` extensively!
*   **File Types**: Currently, the script targets all file types (`-type f`). It does not differentiate between directories, symlinks, or other file system objects.
