# Nightly Digital Dust Bunny Sweeper

## 🧹 Overview

In the digital wasteland, forgotten files accumulate like dust bunnies under a server rack. The `Nightly Digital Dust Bunny Sweeper` is here to help! This utility scans specified directories for files that meet certain criteria (age, size, pattern) and reports them. With an optional `--delete` flag, it can even sweep them away, keeping your digital environment clean and optimized.

It's perfect for automated cleanup tasks, identifying stale logs, temporary build artifacts, or any files that have overstayed their welcome.

## ✨ Features

*   **Age-based cleanup**: Identify files older than a specified number of days.
*   **Size-based filtering**: Target files larger or smaller than a certain size.
*   **Pattern matching**: Include or exclude files based on glob patterns (e.g., `*.log`, `temp_*`).
*   **Dry Run**: Always runs in dry-run mode by default, reporting files without deleting them.
*   **Safe Deletion**: Requires an explicit `--delete` flag to remove files.

## 🚀 Usage

```bash
python3 src/sweeper.py --help
```

```
usage: sweeper.py [-h] --path PATH [--age-days AGE_DAYS] [--min-size MIN_SIZE] [--max-size MAX_SIZE] [--include-pattern INCLUDE_PATTERN] [--exclude-pattern EXCLUDE_PATTERN] [--delete]

A whimsical utility to sweep away old, unused, or temporary 'digital dust bunny' files.

options:
  -h, --help            show this help message and exit
  --path PATH           The root directory to scan for dust bunnies.
  --age-days AGE_DAYS   Files older than this many days will be considered dust bunnies. (default: 30)
  --min-size MIN_SIZE   Files smaller than this many bytes will be considered dust bunnies. (default: 0)
  --max-size MAX_SIZE   Files larger than this many bytes will be considered dust bunnies. (default: 9223372036854775807)
  --include-pattern INCLUDE_PATTERN
                        Glob pattern(s) for files to include (e.g., '*.log', 'temp_*'). Can be specified multiple times.
  --exclude-pattern EXCLUDE_PATTERN
                        Glob pattern(s) for files to exclude (e.g., '*.tmp', 'important_*'). Can be specified multiple times.
  --delete              Actually delete the identified dust bunnies. (DANGER ZONE!)
```

### Examples

1.  **Find all files older than 60 days in `/var/log` (dry run):**

    ```bash
    python3 src/sweeper.py --path /var/log --age-days 60
    ```

2.  **Find and delete `.tmp` files older than 7 days in your home directory:**

    ```bash
    python3 src/sweeper.py --path ~/ --age-days 7 --include-pattern '*.tmp' --delete
    ```

3.  **Identify large log files (over 1GB) but exclude `access.log`:**

    ```bash
    python3 src/sweeper.py --path /var/log --min-size 1073741824 --exclude-pattern 'access.log'
    ```

4.  **Find all files in `~/downloads` that are older than 90 days AND smaller than 10KB:**

    ```bash
    python3 src/sweeper.py --path ~/downloads --age-days 90 --max-size 10240
    ```

## 🛠️ Development

To run tests, navigate to the `utils/nightly-digital-dust-bunny-sweeper` directory and execute:

```bash
python3 -m unittest tests/test_sweeper.py
```
