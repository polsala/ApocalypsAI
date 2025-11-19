# Nightly Digital Dust Bunny Sweeper

## 🧹 Overview

The `nightly-digital-dust-bunny-sweeper` is a whimsical-yet-useful utility designed to keep your digital workspace tidy. It scans specified directories for temporary files, cache folders, and other digital "dust bunnies" that accumulate over time, offering to report or delete them based on configurable patterns and age. Keep your repository lean and mean, ready for the next apocalypse!

## ✨ Features

*   **Configurable Patterns**: Define glob-style patterns (e.g., `*.tmp`, `__pycache__`) to target specific types of files and directories.
*   **Age-Based Cleaning**: Only clean files and directories older than a specified number of days.
*   **Dry Run Mode**: Safely preview what would be deleted without making any changes.
*   **Verbose Output**: Get detailed reports on files and directories being processed.
*   **Self-Contained**: Written in Python, with minimal dependencies, making it easy to integrate.

## 🚀 Usage

To run the sweeper, navigate to the `utils/nightly-digital-dust-bunny-sweeper` directory and execute the `sweeper.py` script.

```bash
python src/sweeper.py <target_directory_1> [target_directory_2 ...] [OPTIONS]
```

### Arguments

*   `<target_dirs>` (required): One or more directories to scan for dust bunnies.

### Options

*   `--patterns <pattern_1> [pattern_2 ...]`: Glob-style patterns for files/directories to clean.
    *   Default: `*.tmp`, `*.log`, `__pycache__`, `*.bak`, `*.swp`, `.DS_Store`, `Thumbs.db`
*   `--age <days>`: Minimum age in days for a file/directory to be considered for cleaning.
    *   Default: `7`
*   `--dry-run`: Report files/directories that *would* be deleted, but do not actually delete them. (Recommended for first runs!)
*   `--verbose`: Print detailed actions during the sweep.

### Examples

1.  **Dry run to see old temporary files in your current directory (and subdirectories):**
    ```bash
    python src/sweeper.py . --patterns "*.tmp" --age 30 --dry-run --verbose
    ```

2.  **Clean up `__pycache__` directories and `.log` files older than 14 days in specific project folders:**
    ```bash
    python src/sweeper.py ~/my_project /var/log/app_logs --patterns "__pycache__" "*.log" --age 14
    ```

3.  **Perform a full sweep with default settings (dry run is OFF by default if not specified):**
    ```bash
    python src/sweeper.py /tmp /var/cache --age 1
    ```
    *(Note: Be cautious when running without `--dry-run` on critical directories!)*

## 🧪 Testing

To ensure the sweeper is working as expected, run the provided unit tests:

```bash
python -m unittest tests/test_sweeper.py
```

The tests use `unittest.mock` to simulate file system operations and time, ensuring deterministic and offline execution.
