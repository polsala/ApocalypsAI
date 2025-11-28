# Nightly Cosmic Dust Collector

## 🌌 Overview

The ApocalypsAI Nightly Cosmic Dust Collector is a whimsical-yet-useful utility designed to help you declutter your digital cosmos. It scans specified directories for "cosmic dust" – small, forgotten files that accumulate over time, such as empty files, old log files, temporary backups, or swap files. By identifying these digital particles, the collector helps you maintain a sparkling clean and efficient workspace.

Currently, this utility focuses on **reporting** detected dust files. Future enhancements may include options for archiving or deleting them.

## ✨ Features

*   **Scans Recursively**: Explores directories and their subdirectories.
*   **Size-Based Detection**: Identifies files smaller than a configurable maximum size.
*   **Extension-Based Detection**: Targets files with specific "temporary" or "log" extensions (e.g., `.tmp`, `.bak`, `.log`).
*   **Empty File Detection**: Always flags empty files as dust, regardless of their extension.
*   **Clear Reporting**: Provides a list of all detected cosmic dust particles with their sizes.

## 🚀 Usage

The utility is a Python 3.11 script that can be run from the command line.

```bash
python src/collector.py <path_to_scan> [OPTIONS]
```

### Arguments:

*   `<path_to_scan>`: The directory path to scan for cosmic dust. This is a required argument.

### Options:

*   `--max-size <bytes>`: Maximum file size in bytes to consider as 'dust'. Files larger than this will be ignored unless they are empty.
    *   Default: `1024` (1 KB)
    *   Example: `--max-size 500` (for files up to 500 bytes)
*   `--extensions <ext1,ext2,...>`: A comma-separated list of file extensions (e.g., `.tmp,.log`) to consider as 'dust'. Empty files are always included, regardless of extension.
    *   Default: `.tmp,.bak,.log,.old,.swp`
    *   Example: `--extensions .cache,.temp`

### Examples:

1.  **Scan your current directory with default settings:**
    ```bash
    python src/collector.py .
    ```

2.  **Scan a specific project directory, looking for files up to 2KB and custom extensions:**
    ```bash
    python src/collector.py /path/to/my/project --max-size 2048 --extensions .temp,.old,.junk
    ```

3.  **Scan your home directory, only looking for empty files and `.log` files, regardless of size (by setting max-size very high):**
    ```bash
    python src/collector.py ~/ --max-size 999999999 --extensions .log
    ```
    *(Note: Empty files are always considered dust, so `--extensions` primarily affects non-empty small files.)*

## 🛠️ Development & Testing

The utility is written in Python 3.11 and uses standard library modules (`os`, `argparse`, `pathlib`).

To run the tests:

```bash
python -m unittest tests/test_collector.py
```

Tests are self-contained and use `unittest.mock` to simulate file system interactions, ensuring determinism and offline execution.
