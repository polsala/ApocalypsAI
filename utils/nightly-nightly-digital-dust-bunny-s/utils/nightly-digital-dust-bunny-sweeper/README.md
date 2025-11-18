# Nightly Digital Dust Bunny Sweeper

## 🧹 Purpose

The `nightly-digital-dust-bunny-sweeper` is a whimsical-yet-useful utility designed to help you reclaim precious digital space by tidying up old, forgotten files – affectionately known as "digital dust bunnies." It scans specified directories, identifies files older than a configurable age, and offers to remove them, ensuring your system stays lean and efficient.

## ✨ Features

*   **Age-based Cleanup**: Target files older than a specified number of days.
*   **Directory Scanning**: Recursively scans one or more directories.
*   **Include/Exclude Patterns**: Fine-tune which files to consider using glob patterns (e.g., `*.log`, `temp_*`).
*   **Dry Run Mode**: Preview which files would be deleted without actually removing them.
*   **Self-Contained**: Pure Python, no external dependencies beyond standard library.

## 🚀 Usage

```bash
python src/sweeper.py --help
```

### Basic Cleanup

To clean files older than 30 days in `/var/log` and `/tmp`:

```bash
python src/sweeper.py --dirs /var/log /tmp --age 30
```

### Dry Run

To see what *would* be deleted without actually deleting anything:

```bash
python src/sweeper.py --dirs /var/log --age 7 --dry-run
```

### With Patterns

To clean `.log` files older than 60 days in `/var/log`, but exclude `important.log`:

```bash
python src/sweeper.py --dirs /var/log --age 60 --include "*.log" --exclude "important.log"
```

### Configuration Options

*   `--dirs <path> [<path> ...]`: One or more directories to scan. (Required)
*   `--age <days>`: Files older than this many days will be considered for deletion. (Default: 30)
*   `--include <pattern> [<pattern> ...]`: Glob patterns for files to *include*. If not specified, all files are considered.
*   `--exclude <pattern> [<pattern> ...]`: Glob patterns for files to *exclude*, even if they match include patterns.
*   `--dry-run`: Perform a dry run, printing files that *would* be deleted without actually deleting them.
*   `--verbose`: Print more detailed information during the scan.

## 🛠️ Development

The utility is written in Python 3.11 and uses only standard library modules.

### Running Tests

```bash
python -m unittest tests/test_sweeper.py
```
