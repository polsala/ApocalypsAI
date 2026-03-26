# Nightly Wasteland Cache Cleaner

## 📜 Description

In the desolate digital wasteland, your storage caches can quickly become cluttered with forgotten relics and resource-hogging data. The `Nightly Wasteland Cache Cleaner` is a whimsical-yet-useful Bash utility designed to help survivors (and their systems) manage their digital hoarding. It scans a specified directory for files that are either too old ("ancient relics") or too large ("resource hogs") and provides options to list them or purge them from existence. Keep your caches lean and mean for optimal survival!

## 🚀 Usage

### Prerequisites

*   Bash (version 4.0 or higher recommended)
*   `find`, `stat`, `du`, `rm`, `grep`, `cut`, `mktemp`, `dd` (standard Linux/macOS utilities)

### Running the Cleaner

Navigate to the `nightly-wasteland-cache-cleaner` directory and run the script:

```bash
./src/cache_cleaner.sh <directory> [--mode old|large] [--threshold <value>] [--action list|delete]
```

#### Arguments:

*   `<directory>` (required): The path to the cache (directory) you want to scan.
*   `--mode` (optional):
    *   `old` (default): Find files based on their age.
    *   `large`: Find files based on their size.
*   `--threshold` (optional):
    *   For `--mode old`: Specify age, e.g., `30d` for files older than 30 days. Default is `30d`.
    *   For `--mode large`: Specify size, e.g., `100M` for files larger than 100 MB, `1G` for 1 GB. Default is `100M`.
*   `--action` (optional):
    *   `list` (default): Simply list the identified files.
    *   `delete`: Permanently remove the identified files. **Use with caution!**

### Examples:

1.  **List all files older than 60 days in your `/tmp/survival_cache`:**
    ```bash
    ./src/cache_cleaner.sh /tmp/survival_cache --mode old --threshold 60d
    ```

2.  **Identify all files larger than 500 MB in your current directory:**
    ```bash
    ./src/cache_cleaner.sh . --mode large --threshold 500M
    ```

3.  **Purge (delete) all files older than 90 days in your `/var/log/ancient_logs` directory:**
    ```bash
    ./src/cache_cleaner.sh /var/log/ancient_logs --mode old --threshold 90d --action delete
    ```

4.  **List files larger than 2GB in a specific user's data directory (using default mode/threshold for 'old' if not specified):**
    ```bash
    ./src/cache_cleaner.sh /home/survivor/data --mode large --threshold 2G
    ```

## 🧪 Tests

To run the tests, navigate to the utility's root directory and execute the test script:

```bash
./tests/test_cache_cleaner.sh
```

The tests create a temporary directory, generate mock files with specific ages and sizes, and then run the `cache_cleaner.sh` script against them, asserting on the output and file system changes. This ensures the utility functions as expected without affecting your actual files.
