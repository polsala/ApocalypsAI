# Nightly Data Debris Duster

## 🧹 Overview

The Nightly Data Debris Duster is a command-line utility designed to help you keep your digital workspace tidy in the post-apocalyptic landscape. It scans a specified directory for files older than a given threshold (based on their last modification time) and provides options to list them or delete them. Think of it as a digital broom for your data rubble!

## ✨ Features

*   **Age-based Filtering**: Identify files older than a specified number of days.
*   **Directory Scanning**: Recursively scans directories for old files.
*   **Dry Run Mode**: List files that *would* be deleted without actually removing them.
*   **Safe Deletion**: Only deletes files when explicitly confirmed.

## 🚀 Usage

```bash
python src/duster.py --path /path/to/your/data --days 30
```

### Arguments:

*   `--path <directory>` (required): The root directory to scan for old files.
*   `--days <int>` (required): The age threshold in days. Files modified more than this many days ago will be considered "debris".
*   `--delete` (optional): If provided, the utility will prompt for confirmation before deleting the identified files. **Use with caution!**
*   `--verbose` (optional): Print more detailed output during scanning.

### Examples:

1.  **List files older than 90 days in `/home/survivor/temp` (dry run):**
    ```bash
    python src/duster.py --path /home/survivor/temp --days 90
    ```

2.  **Delete files older than 30 days in `/var/log/old_logs` (with confirmation):**
    ```bash
    python src/duster.py --path /var/log/old_logs --days 30 --delete
    ```

## 🛠️ Development

### Requirements

*   Python 3.8+

### Running Tests

```bash
python -m unittest tests/test_duster.py
```
