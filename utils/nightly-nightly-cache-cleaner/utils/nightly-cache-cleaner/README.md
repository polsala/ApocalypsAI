# Nightly Cache Cleaner of Forgotten Files

## 🧹 Overview

The Nightly Cache Cleaner is a diligent digital janitor designed to scour your specified directories for temporary, log, backup, and other forgotten files that accumulate over time. It helps reclaim precious disk space and keeps your project directories tidy, preventing the digital equivalent of dust bunnies from taking over.

## ✨ Features

*   **Pattern-based Cleaning**: Define glob patterns (e.g., `*.tmp`, `*.log`, `~*`) to target specific file types.
*   **Age-based Filtering**: Only clean files older than a specified number of days, ensuring you don't accidentally remove recently used items.
*   **Dry Run Mode**: Preview which files would be deleted without actually removing them, for peace of mind.
*   **Confirmation Prompt**: Requires explicit confirmation before deletion (unless `--force` is used).
*   **Self-contained**: A single Python script with no external dependencies beyond standard library modules.

## 🚀 Usage

```bash
python src/cleaner.py --path /path/to/clean --patterns "*.tmp,*.log,*.bak,~*#*" --age 7 --dry-run
```

### Arguments:

*   `--path <directory>`: **Required**. The root directory to start cleaning from. The cleaner will recursively scan this directory.
*   `--patterns <glob_patterns>`: **Required**. A comma-separated list of glob patterns (e.g., `*.tmp,*.log`). Files matching any of these patterns will be considered for deletion.
*   `--age <days>`: **Required**. Files older than this many days will be considered for deletion.
*   `--dry-run`: If present, the utility will only list files that *would* be deleted, without actually removing them.
*   `--force`: If present, skips the confirmation prompt before deleting files. Use with caution!

## 🛠️ Development

The cleaner is written in Python 3.11 and uses only standard library modules.

### Running Tests

```bash
python -m unittest tests/test_cleaner.py
```
