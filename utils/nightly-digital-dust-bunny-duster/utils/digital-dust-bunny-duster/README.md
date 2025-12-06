# Digital Dust Bunny Duster

## 🧹 What it Does

The Digital Dust Bunny Duster is a whimsical yet highly practical utility designed to help you reclaim precious disk space by identifying and optionally purging common temporary and cache files/directories, affectionately known as "digital dust bunnies."

It scans specified paths for build artifacts, Python caches, Node.js modules, log files, and other transient data that tends to accumulate over time, providing a report and the option to clean them up.

## ✨ Features

*   **Comprehensive Scanning**: Detects a wide range of common cache and temporary files/folders across various programming ecosystems (Python, Node.js, Java/Rust build artifacts, macOS/Windows specific junk).
*   **Age-Based Filtering**: Optionally filter log files and other temporary files by their modification age.
*   **Dry Run Mode**: See exactly what would be deleted before committing to any changes.
*   **Safe Deletion**: Carefully removes identified "dust bunnies" without touching critical project files.
*   **Self-Contained**: Written in Python 3.11 with only standard library dependencies.

## 🚀 How to Use

```bash
python src/duster.py --path /path/to/your/project --dry-run
```

### Arguments:

*   `--path <directory>` (required): The root directory to start scanning from.
*   `--delete`: If provided, the utility will actually delete the found dust bunnies. **Use with caution!**
*   `--dry-run`: If provided, the utility will only report what it *would* delete, without making any changes. (Default if `--delete` is not present).
*   `--age-days <int>`: For files like `.log` or `.tmp`, only consider them dust bunnies if they are older than this many days. Defaults to 7 days.

### Examples:

1.  **Scan your current directory for dust bunnies (dry run):**
    ```bash
    python src/duster.py --path . --dry-run
    ```

2.  **Scan a specific project directory and delete items older than 30 days:**
    ```bash
    python src/duster.py --path /home/user/my_big_project --delete --age-days 30
    ```

3.  **Just list all dust bunnies in a directory, regardless of age for log/tmp files:**
    ```bash
    python src/duster.py --path /var/log --age-days 0 --dry-run
    ```

## 🛠️ Development

The `duster.py` script is a standalone Python 3.11 application.
Tests are located in `tests/test_duster.py` and can be run using `pytest` or `unittest`.

```bash
python -m unittest tests/test_duster.py
```
