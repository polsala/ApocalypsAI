# Nightly Digital Detritus Disposer

## 🧹 What is this?

The ApocalypsAI Nightly Digital Detritus Disposer is a whimsical yet practical utility designed to help you keep your digital workspace tidy. Over time, development environments, download folders, and temporary directories accumulate a lot of 'digital detritus' – old log files, forgotten build artifacts, stale caches, and other files that are no longer needed. This utility helps you identify and optionally remove these forgotten files.

Think of it as a diligent digital janitor, sweeping away the dust bunnies of your filesystem before they become an apocalyptic pile.

## ✨ Features

*   **Directory Scanning**: Recursively scans a specified directory for files.
*   **Age-based Filtering**: Identifies files older than a configurable number of days.
*   **Dry Run Mode**: Lists files that *would* be deleted without actually removing them.
*   **Deletion Mode**: Safely removes identified old files.

## 🚀 How to Use

### Prerequisites

*   Python 3.6+ (tested with 3.11)

### Running the Disposer

1.  Navigate to the utility's directory:
    ```bash
    cd utils/nightly-digital-detritus-disposer
    ```

2.  **Perform a Dry Run (Recommended First!)**
    This will list all files older than 30 days in the `/tmp/my_project` directory without deleting anything.
    ```bash
    python src/disposer.py --path /tmp/my_project --age 30 --dry-run
    ```
    You can specify any directory you want to clean.

3.  **Delete Files**
    Once you're confident with the dry run output, you can proceed with deletion. **Use with caution!**
    ```bash
    python src/disposer.py --path /tmp/my_project --age 30 --delete
    ```

    *   `--path <directory>`: The root directory to scan (required).
    *   `--age <days>`: Files older than this many days will be considered detritus (default: 30).
    *   `--dry-run`: Only list files, do not delete (default if `--delete` is not specified).
    *   `--delete`: Actually delete the identified files. **Cannot be used with `--dry-run`**.

## 🧪 Testing

To run the tests for this utility:

```bash
cd utils/nightly-digital-detritus-disposer
python -m unittest tests/test_disposer.py
```
