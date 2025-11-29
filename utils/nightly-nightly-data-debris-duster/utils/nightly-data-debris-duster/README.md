# Nightly Data Debris Duster

## 🧹 Overview

The **Nightly Data Debris Duster** is a whimsical-yet-useful utility designed to help you keep your digital environment tidy by identifying and optionally removing old, unused files – what we affectionately call "data debris." In the post-apocalyptic digital landscape, every byte counts, and this tool ensures your storage isn't cluttered with forgotten relics.

It scans specified directories for files that haven't been modified in a long time, allowing you to perform a dry run to see what would be removed, or to proceed with actual deletion.

## ✨ Features

*   **Age-based Identification**: Finds files older than a specified number of days.
*   **Dry Run Mode**: Preview which files would be deleted without actually removing them.
*   **Recursive Scanning**: Option to scan subdirectories for deeper debris removal.
*   **Simple & Self-contained**: A single Python script with minimal dependencies.

## 🚀 Usage

### Prerequisites

*   Python 3.6+ (tested with 3.11)

### Running the Duster

Navigate to the `src` directory within `nightly-data-debris-duster` and run the `duster.py` script.

```bash
cd utils/nightly-data-debris-duster/src
python duster.py <directory_to_scan> [options]
```

#### Arguments:

*   `<directory_to_scan>`: The path to the directory you want to scan for data debris. This is a required argument.

#### Options:

*   `--age <days>`: (Optional) The minimum age in days for a file to be considered "debris." Files older than this threshold will be flagged. Default is `90` days.
    *   Example: `--age 30` (finds files older than 30 days)
*   `--delete`: (Optional) Use this flag to actually delete the identified files. **By default, the utility performs a dry run and only lists files without deleting them.**
*   `--recursive`: (Optional) Use this flag to scan subdirectories within the specified directory. By default, only the top-level directory is scanned.

### Examples:

1.  **Dry run, scan current directory for files older than 90 days (default):**
    ```bash
    python duster.py .
    ```

2.  **Dry run, scan `/tmp/my_downloads` for files older than 30 days, recursively:**
    ```bash
    python duster.py /tmp/my_downloads --age 30 --recursive
    ```

3.  **Actually delete files older than 180 days in `/var/log/old_logs` (non-recursive):**
    ```bash
    python duster.py /var/log/old_logs --age 180 --delete
    ```

4.  **Actually delete files older than 7 days in `/home/user/temp` (recursive):**
    ```bash
    python duster.py /home/user/temp --age 7 --delete --recursive
    ```

## 🧪 Testing

To run the automated tests, navigate to the `tests` directory and execute the test script:

```bash
cd utils/nightly-data-debris-duster/tests
python -m unittest test_duster.py
```

All tests are deterministic and use mocks to simulate file system interactions and time, ensuring consistent results without touching your actual files.
