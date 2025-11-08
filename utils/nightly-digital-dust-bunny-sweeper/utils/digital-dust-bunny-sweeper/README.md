# Digital Dust Bunny Sweeper

## Overview

The `digital-dust-bunny-sweeper` is your friendly neighborhood digital janitor! This utility helps you reclaim precious disk space and maintain a tidy file system by sniffing out those forgotten, old, or temporary files and folders – your 'digital dust bunnies'. It scans specified directories, identifies potential clutter based on age or file patterns, and presents them to you for review. You can then choose to sweep them away or keep them for another day.

## Features

*   **Age-based scanning**: Find files and directories not accessed or modified within a configurable timeframe.
*   **Pattern matching**: Identify files by common temporary file extensions (e.g., `.log`, `.tmp`, `.bak`) or custom patterns.
*   **Interactive review**: Get a clear list of identified 'dust bunnies' before any action is taken.
*   **Dry-run mode**: See what would be swept without actually deleting anything.
*   **Confirmation**: Requires explicit confirmation before permanent deletion.
*   **Whimsical output**: Enjoy a bit of fun while decluttering!

## Installation

This utility is self-contained and written in Python 3.11+. No external dependencies are strictly required beyond the standard library.

To run it, simply navigate to the `utils/digital-dust-bunny-sweeper/` directory and execute the `src/sweeper.py` script.

## Usage

```bash
python src/sweeper.py --path <directory_to_scan> [--age <days>] [--patterns <pattern1> <pattern2> ...] [--dry-run] [--delete]
```

### Arguments:

*   `--path <directory>`: **Required**. The root directory to start scanning for dust bunnies.
*   `--age <days>`: Optional. Files/directories not accessed or modified in this many days or more will be flagged. Default: `30`.
*   `--patterns <pattern1> <pattern2> ...`: Optional. Space-separated list of glob patterns (e.g., `*.log`, `temp_*`, `~*`). Files/directories matching these patterns will be flagged. Default: `*.log *.tmp *.bak`.
*   `--dry-run`: Optional. If present, the utility will only list what *would* be deleted, without performing any actual deletions. This is the default behavior if `--delete` is not specified.
*   `--delete`: Optional. If present, after listing, the utility will prompt for confirmation to delete the identified items. **Use with caution!**

### Examples:

Scan your downloads folder for items older than 90 days (dry run):
```bash
python src/sweeper.py --path ~/Downloads --age 90 --dry-run
```

Scan a project directory for log files and temporary folders, then delete with confirmation:
```bash
python src/sweeper.py --path ~/my_project --patterns "*.log" "temp_*" --delete
```

## Development & Testing

To run the tests, navigate to the utility's root directory and execute:

```bash
python -m unittest tests/test_sweeper.py
```
