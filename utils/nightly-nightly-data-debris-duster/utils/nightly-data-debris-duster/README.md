# Nightly Data Debris Duster

## 🧹 Overview

The Nightly Data Debris Duster is a whimsical-yet-useful utility designed to help you keep your digital "wasteland" tidy. In the post-apocalyptic landscape of your file system, old, forgotten files accumulate like so much digital rubble. This tool helps you identify and optionally remove files that haven't been touched in a specified number of days, freeing up precious storage and decluttering your directories.

Think of it as a robotic scavenger, sifting through the detritus of your data, making way for new growth (or at least, new files).

## ✨ Features

*   **Age-based Identification**: Scans a specified directory for files older than a given number of days (based on last modification time).
*   **Preview Mode**: Lists identified "debris" without deleting anything, allowing for review.
*   **Deletion Mode**: Safely removes identified old files after confirmation (or forced deletion).
*   **Recursive Scanning**: Can traverse subdirectories to find hidden digital junk.

## 🚀 Usage

```bash
python src/duster.py --path <directory_to_clean> --days <N_days_old> [--delete] [--recursive] [--force]
```

### Arguments:

*   `--path <directory>`: The root directory to start scanning for old files. (Required)
*   `--days <N>`: The minimum age in days for a file to be considered "debris". Files modified `N` days ago or earlier will be targeted. (Required)
*   `--delete`: If present, identified files will be deleted. **Use with caution!** Without this flag, files are only listed. (Optional)
*   `--recursive`: If present, the duster will scan subdirectories as well. (Optional)
*   `--force`: If present with `--delete`, files will be deleted without a confirmation prompt. (Optional)

### Examples:

*   **List files older than 30 days in the current directory:**
    ```bash
    python src/duster.py --path . --days 30
    ```
*   **Delete files older than 90 days in `/tmp/old_logs` recursively, with confirmation:**
    ```bash
    python src/duster.py --path /tmp/old_logs --days 90 --delete --recursive
    ```
*   **Force delete files older than 7 days in `~/downloads` without prompt:**
    ```bash
    python src/duster.py --path ~/downloads --days 7 --delete --force
    ```

## 🛠️ Development

The `duster.py` script is a self-contained Python 3.11 utility. It uses standard library modules only.

### Running Tests

To ensure the duster is functioning correctly and not accidentally deleting vital data (unless instructed!), run the provided tests:

```bash
python -m unittest tests/test_duster.py
```
