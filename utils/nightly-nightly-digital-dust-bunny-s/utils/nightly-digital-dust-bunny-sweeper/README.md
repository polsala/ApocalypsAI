# Nightly Digital Dust Bunny Sweeper

## 🧹 Overview

The `nightly-digital-dust-bunny-sweeper` is a whimsical yet practical utility designed to help you keep your project directories clean and tidy. Like a diligent digital janitor, it identifies and optionally removes "dust bunnies" – old, unused, or empty files and directories – that accumulate over time, ensuring your workspace remains pristine and efficient.

## ✨ Features

*   **Identify Old Files**: Scans for files older than a specified number of days.
*   **Identify Empty Directories**: Finds directories that contain no files or subdirectories.
*   **Pattern Matching**: Allows specifying file patterns (e.g., `*.log`, `*.tmp`, `~*`) to target specific types of transient files.
*   **Dry Run Mode**: Safely preview what would be cleaned without making any changes.
*   **Cleanup Mode**: Execute the cleanup operation to remove identified items.
*   **Self-contained**: Written in Python, with minimal dependencies, making it easy to integrate.

## 🚀 Usage

The utility is a command-line tool.

```bash
python src/sweeper.py --help
```

### Examples:

1.  **Dry run to find all empty directories and files older than 30 days in the current directory:**
    ```bash
    python src/sweeper.py --path . --age 30 --dry-run
    ```

2.  **Clean up all `.log` and `.tmp` files in a specific `temp/` directory:**
    ```bash
    python src/sweeper.py --path ./temp --patterns "*.log,*.tmp" --clean
    ```

3.  **Dry run to find only empty directories in a project's `build/` folder:**
    ```bash
    python src/sweeper.py --path ./build --empty-dirs-only --dry-run
    ```

4.  **Clean up all identified items (empty directories, files older than 7 days, and `*.bak` files) in the current directory:**
    ```bash
    python src/sweeper.py --path . --age 7 --patterns "*.bak" --clean
    ```

### Arguments:

*   `--path <directory>` (required): The root directory to scan.
*   `--age <days>` (optional): Files older than this many days will be considered for cleanup.
*   `--patterns <comma-separated-patterns>` (optional): Comma-separated glob patterns (e.g., `*.log,*.tmp`) for files to consider.
*   `--empty-dirs-only` (optional): Only scan for and clean up empty directories.
*   `--dry-run`: Perform a dry run, listing what *would* be cleaned without making changes.
*   `--clean`: Execute the cleanup operation, deleting identified items. **Use with caution!**

## 🛠️ Development

### Requirements

*   Python 3.8+ (tested with 3.11)

### Running Tests

To ensure the sweeper is working as expected, run the provided tests:

```bash
python -m unittest tests/test_sweeper.py
```
