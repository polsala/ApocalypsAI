# ApocalypsAI Nightly Cache Purifier

## 🧹 Whimsical Utility: Nightly Cache Purifier

In the chaotic aftermath, digital debris accumulates, slowing down even the most resilient systems. The Nightly Cache Purifier is your automated solution to keep your digital environment pristine, clearing out the accumulated detritus of old cache files and empty directories. Think of it as a diligent scavenger bot, tidying up the forgotten corners of your file system.

## ✨ Features

*   **Automated Cleanup**: Scans common cache directories (OS-specific) for old files.
*   **Age-Based Deletion**: Configurable to remove files older than a specified number of days.
*   **Empty Directory Removal**: Automatically cleans up directories that become empty after file deletion.
*   **Dry Run Mode**: Preview what would be deleted without making any changes.
*   **Targeted Cleaning**: Option to clean a specific directory instead of default cache paths.
*   **Cross-Platform**: Supports Linux, macOS, and Windows common cache locations.

## 🚀 How to Run

This utility is a Python 3.x script.

1.  **Navigate to the utility directory**:
    ```bash
    cd utils/nightly-cache-purifier
    ```

2.  **Run the purifier**:

    *   **Default cleanup (dry run, 7 days old)**:
        ```bash
        python3 src/purifier.py --dry-run
        ```
        This will list all files and empty directories that *would* be deleted without actually removing them.

    *   **Actual cleanup (7 days old)**:
        ```bash
        python3 src/purifier.py
        ```
        **Use with caution!** This will permanently delete files and empty directories older than 7 days from common cache locations.

    *   **Custom age (e.g., 30 days old)**:
        ```bash
        python3 src/purifier.py --age-days 30
        ```

    *   **Clean a specific directory (e.g., `/var/log/old_logs`)**:
        ```bash
        python3 src/purifier.py --target-dir /var/log/old_logs --age-days 14
        ```

    *   **Combined options**:
        ```bash
        python3 src/purifier.py --dry-run --age-days 1 --target-dir ~/Downloads/temp_files
        ```

## 🧪 Testing

To ensure the purifier is always ready for its nightly rounds, run the self-contained tests:

1.  **Navigate to the utility directory**:
    ```bash
    cd utils/nightly-cache-purifier
    ```
2.  **Run the tests**:
    ```bash
    python3 -m unittest tests/test_purifier.py
    ```

The tests use mocks to simulate file system operations and system time, ensuring deterministic and offline validation of the cleanup logic without affecting your actual files.
