# Nightly Cache Cleaner of Forgotten Files

## 🧹 Purpose

The `Nightly Cache Cleaner` is a whimsical-yet-useful utility designed to help you reclaim disk space by identifying and archiving files that are either too old ("forgotten") or excessively large ("bloated"). It scans a specified directory, finds files matching your criteria, and offers to move them to a designated archive location, keeping your active workspaces tidy without permanent deletion.

## ✨ Features

*   **Age-based Stale File Detection**: Identify files not modified within a configurable number of days.
*   **Size-based Bloated File Detection**: Pinpoint files exceeding a specified size threshold.
*   **Recursive Scanning**: Traverses subdirectories to ensure no forgotten file escapes its gaze.
*   **Safe Archiving**: Moves identified files to a separate archive directory, preventing accidental data loss.
*   **Collision Handling**: Automatically renames archived files if a name conflict occurs in the archive directory (e.g., `file.txt` becomes `file_YYYYMMDDHHMMSS.txt`).

## 🚀 Usage

This utility is a Python 3.11 script.

### Prerequisites

*   Python 3.11+

### Running the Cleaner

```bash
python src/cleaner.py <directory_to_scan> [options]
```

**Arguments:**

*   `<directory_to_scan>`: The root directory where the cleaner will start looking for stale files.

**Options:**

*   `--age <days>`: Files older than this many days will be considered stale.
    *   Default: `30` days.
*   `--size <MB>`: Files larger than this many megabytes will be considered stale.
    *   Default: `100` MB.
*   `--archive-dir <path>`: The directory where identified stale files will be moved. If this option is omitted, the utility will only list the stale files found, without moving them.

### Examples:

1.  **List all files in `/tmp/my_cache` older than 60 days or larger than 500MB:**
    ```bash
    python src/cleaner.py /tmp/my_cache --age 60 --size 500
    ```

2.  **Archive files in `/home/user/downloads` older than 90 days (default size) to `/home/user/archives/downloads_cleanup`:**
    ```bash
    python src/cleaner.py /home/user/downloads --age 90 --archive-dir /home/user/archives/downloads_cleanup
    ```

3.  **Archive files in `/var/log` larger than 2GB (default age) to `/var/log/old_logs`:**
    ```bash
    python src/cleaner.py /var/log --size 2048 --archive-dir /var/log/old_logs
    ```

## 🧪 Testing

To run the tests for this utility, navigate to the `utils/nightly-cache-cleaner` directory and execute:

```bash
python -m unittest tests/test_cleaner.py
```

The tests are designed to be deterministic and do not interact with the actual file system, relying on Python's `unittest.mock` library to simulate file system operations and time-related functions.
