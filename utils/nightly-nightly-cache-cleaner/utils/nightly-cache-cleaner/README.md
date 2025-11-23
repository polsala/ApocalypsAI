# Nightly Cache Cleaner of Forgotten Files

## 🧹 Description

The `nightly-cache-cleaner` is a diligent utility designed to sweep away the digital dust bunnies and forgotten files that accumulate in your project directories. It helps maintain a lean and efficient workspace by identifying and optionally removing old or temporary files based on their age and specified patterns. Think of it as your personal digital janitor, ensuring your development environment remains pristine and performant.

## ✨ Features

*   **Age-based Cleanup**: Target files older than a specified number of days.
*   **Pattern Matching**: Use glob-style patterns to identify specific file types or names (e.g., `*.log`, `__pycache__`).
*   **Multiple Paths**: Scan multiple directories simultaneously.
*   **Dry Run Mode**: Preview which files would be deleted without actually removing them.
*   **Force Deletion**: Automate cleanup without interactive prompts.

## 🚀 Usage

```bash
python3 src/cleaner.py --help
```

```
usage: cleaner.py [-h] --paths PATHS [PATHS ...] [--age-days AGE_DAYS] [--patterns PATTERNS [PATTERNS ...]] [--dry-run] [--force]

Clean old or temporary files from specified directories.

options:
  -h, --help            show this help message and exit
  --paths PATHS [PATHS ...]
                        One or more directories to scan for old files.
  --age-days AGE_DAYS   Delete files older than this many days. (default: 30)
  --patterns PATTERNS [PATTERNS ...]
                        Glob-style patterns for files to consider (e.g., '*.log', '__pycache__'). If not specified, all files older than --age-days are considered.
  --dry-run             Perform a dry run, only printing files that would be deleted without actually deleting them.
  --force               Bypass confirmation prompt and delete files immediately (use with caution).
```

### Examples:

1.  **Dry run to find all files older than 60 days in `~/my_project/build` and `~/my_project/logs`:**
    ```bash
    python3 src/cleaner.py --paths ~/my_project/build ~/my_project/logs --age-days 60 --dry-run
    ```

2.  **Delete all `.log` files older than 7 days in the current directory and its subdirectories:**
    ```bash
    python3 src/cleaner.py --paths . --age-days 7 --patterns '*.log' --force
    ```

3.  **Clean `__pycache__` directories and `.tmp` files in a specific project, interactively:**
    ```bash
    python3 src/cleaner.py --paths /var/www/my_app --patterns '__pycache__' '*.tmp'
    ```

## 🛠️ Development

To run tests:

```bash
python3 -m unittest tests/test_cleaner.py
```
