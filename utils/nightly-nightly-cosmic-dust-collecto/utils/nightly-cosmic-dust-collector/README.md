# Nightly Cosmic Dust Collector

## 🌌 Overview

The Nightly Cosmic Dust Collector is a whimsical-yet-useful utility designed to help you declutter your filesystem by identifying and managing 'cosmic dust' – those small, forgotten, or empty files that accumulate over time. Think of it as a digital vacuum cleaner for your directories, ensuring your digital space remains pristine and efficient.

It scans a specified directory for files smaller than a given threshold and offers options to simply list them, move them to an archive, or permanently delete them.

## ✨ Features

*   **Customizable Threshold**: Define what constitutes 'cosmic dust' by setting a maximum file size.
*   **Multiple Actions**: Choose to `list`, `archive`, or `delete` identified files.
*   **Dry Run Mode**: Preview changes before committing to any actions.
*   **Recursive Scan**: Traverses subdirectories to find hidden dust.

## 🚀 Usage

This utility is a Python 3.11 script. You can run it directly from its `src` directory.

```bash
python3 src/dust_collector.py --help
```

### Arguments:

*   `--path <directory>` (required): The root directory to scan for cosmic dust.
*   `--threshold <bytes>` (optional, default: 1024): Maximum file size in bytes to consider as 'cosmic dust'. Files larger than this will be ignored.
*   `--action <list|archive|delete>` (optional, default: `list`): The action to perform on identified files.
    *   `list`: Simply print the paths of the files found.
    *   `archive`: Move the files to a specified archive directory.
    *   `delete`: Permanently delete the files.
*   `--archive-dir <directory>` (required if action is `archive`): The directory where files will be moved when archiving.
*   `--dry-run` (optional): If set, no files will be moved or deleted. The script will only report what *would* happen.

### Examples:

1.  **List all files smaller than 500 bytes in `/tmp/my_project` (dry run):**
    ```bash
    python3 src/dust_collector.py --path /tmp/my_project --threshold 500 --action list --dry-run
    ```

2.  **Archive all files smaller than 2KB in `/home/user/downloads` to `/home/user/archive/dust`:**
    ```bash
    python3 src/dust_collector.py --path /home/user/downloads --threshold 2048 --action archive --archive-dir /home/user/archive/dust
    ```

3.  **Delete all empty files (threshold 0 bytes) in `/var/log/old_logs`:**
    ```bash
    python3 src/dust_collector.py --path /var/log/old_logs --threshold 0 --action delete
    ```

## 🛠️ Development

To run tests, navigate to the `nightly-cosmic-dust-collector` directory and execute:

```bash
python3 -m unittest tests/test_dust_collector.py
```
