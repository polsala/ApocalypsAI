# Nightly Digital Dust Bunny Sweeper

## 🧹 What is this?

The Digital Dust Bunny Sweeper is a whimsical-yet-useful utility designed to help you keep your digital workspace tidy. It identifies and, optionally, removes "digital dust bunnies" – those old, forgotten, and often temporary files that accumulate in your directories over time. Think of it as a tiny, automated Roomba for your file system!

## ✨ Features

*   **Age-based Cleanup**: Target files older than a specified number of days.
*   **Pattern Matching**: Focus on specific file types (e.g., `.log`, `.tmp`, backup files like `~*`).
*   **Dry Run Mode**: See what files *would* be deleted before actually removing them, ensuring peace of mind.
*   **Directory Scan**: Scan one or more specified directories.
*   **Self-contained**: A single Python script with no external dependencies beyond the standard library.

## 🚀 How to Use

### Prerequisites

*   Python 3.6+ (tested with 3.11)

### Running the Sweeper

1.  Navigate to the `utils/nightly-digital-dust-bunny-sweeper/src` directory.
2.  Run the `sweeper.py` script from your terminal.

```bash
python sweeper.py --help
```

#### Example: Dry Run (recommended first step!)

This command will list all `.log` and `.tmp` files older than 30 days in `/var/log` and `~/temp_files` without deleting anything.

```bash
python sweeper.py --dirs /var/log ~/temp_files --age 30 --patterns "*.log" "*.tmp" --dry-run
```

#### Example: Actual Cleanup

**⚠️ Use with caution! This will delete files.**

This command will delete all `.bak` files older than 7 days in your current directory.

```bash
python sweeper.py --dirs . --age 7 --patterns "*.bak"
```

#### Arguments:

*   `--dirs <path> [<path> ...]`: One or more directories to scan. Required.
*   `--age <days>`: Files older than this many days will be considered. Default: `30`.
*   `--patterns <pattern> [<pattern> ...]`: One or more glob patterns (e.g., `*.log`, `temp_*`). Default: `*` (all files).
*   `--dry-run`: If present, only list files that would be deleted, do not actually delete them. Default: `False`.

## 🛠️ Development & Testing

To run the tests, navigate to the `utils/nightly-digital-dust-bunny-sweeper/tests` directory and execute `pytest` (or `python -m unittest` if `pytest` is not installed).

```bash
cd utils/nightly-digital-dust-bunny-sweeper/tests
python -m unittest test_sweeper.py
```
