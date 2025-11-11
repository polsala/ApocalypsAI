# Digital Dust Bunny Sweeper

## 🧹 Purpose

In the grand scheme of preparing for the inevitable, a clean digital workspace is paramount. The `digital-dust-bunny-sweeper` is a whimsical yet practical utility designed to help you identify and optionally purge those forgotten, redundant, or simply ancient files – your 'digital dust bunnies' – that accumulate over time. Keep your repositories lean and your local drives pristine, ready for whatever the future holds!

## ✨ Features

*   **Age-based Filtering**: Find files older than a specified number of days.
*   **Pattern Matching**: Target specific file types (e.g., `.log`, `.tmp`, `~*` backup files).
*   **Dry Run Mode**: Preview which files would be affected before any deletion occurs.
*   **Recursive Scanning**: Scans subdirectories for hidden dust bunnies.

## 🚀 Usage

```bash
python src/sweeper.py --path <directory> [--age <days>] [--patterns <pattern1> <pattern2> ...] [--dry-run] [--delete]
```

### Arguments:

*   `--path <directory>`: **Required**. The root directory to start sweeping for dust bunnies.
*   `--age <days>`: Optional. Only consider files older than this many days. Default is 30 days.
*   `--patterns <pattern1> <pattern2> ...`: Optional. One or more glob patterns (e.g., `*.log`, `*.tmp`, `~*`) to match files. If not provided, all files (subject to age) are considered.
*   `--dry-run`: Optional. Perform a dry run, listing files that *would* be deleted without actually deleting them. This is the default behavior if `--delete` is not specified.
*   `--delete`: Optional. **CAUTION!** Actually delete the identified files. Use with care, preferably after a `--dry-run`.

### Examples:

1.  **Find all files older than 60 days in the current directory (dry run):**
    ```bash
    python src/sweeper.py --path . --age 60
    ```

2.  **Find and delete all `.log` and `.tmp` files older than 7 days in a specific project directory:**
    ```bash
    python src/sweeper.py --path /path/to/my/project --age 7 --patterns "*.log" "*.tmp" --delete
    ```

3.  **List all files matching `*.bak` or `~*` in a directory, regardless of age (dry run):**
    ```bash
    python src/sweeper.py --path /var/log --patterns "*.bak" "~*"
    ```

## 🛠️ Development

This utility is written in Python 3.11 and is self-contained. No external dependencies are required beyond the standard library.

## 🧪 Testing

To run the tests, navigate to the `utils/digital-dust-bunny-sweeper` directory and execute:

```bash
python -m unittest tests/test_sweeper.py
```
