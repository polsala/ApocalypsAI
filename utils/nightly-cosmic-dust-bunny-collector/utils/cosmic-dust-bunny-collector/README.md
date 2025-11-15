# Cosmic Dust Bunny Collector

## Overview

The `cosmic-dust-bunny-collector` is a whimsical yet practical utility designed to help you maintain a clean and organized digital workspace. It scans specified directories for 'cosmic dust bunnies' – temporary files, log files, backup files, or simply old files that are no longer needed – and provides options to list them or delete them. Keep your project directories pristine, ready for any cosmic eventuality!

## Features

*   **Pattern-based Scanning**: Identify files by common temporary file patterns (e.g., `.tmp`, `.log`, `~`, `#`).
*   **Age-based Filtering**: Filter files older than a specified number of days.
*   **Dry Run Mode**: Safely preview which files would be affected without making any changes.
*   **Deletion Mode**: Permanently remove identified 'dust bunnies'.
*   **Recursive Scanning**: Traverse subdirectories to find hidden clutter.

## Installation

This utility is self-contained and requires Python 3.8+.

```bash
# No installation needed, just run the script directly.
cd utils/cosmic-dust-bunny-collector/src
python collector.py --help
```

## Usage

```bash
python utils/cosmic-dust-bunny-collector/src/collector.py [OPTIONS] <directory>
```

### Arguments

*   `<directory>`: The path to the directory to scan.

### Options

*   `--patterns <pattern1> <pattern2> ...`: Space-separated list of glob patterns to match (e.g., `*.tmp` `*.log` `*~`). Defaults to common patterns.
*   `--age <days>`: Only consider files older than this many days. Defaults to 0 (all files matching patterns).
*   `--delete`: **CAUTION**: Enable this flag to actually delete the files. By default, it runs in dry-run mode.
*   `--verbose`: Print more detailed information during the scan.
*   `--help`: Show the help message and exit.

### Examples

1.  **Dry run to find all common dust bunnies in the current directory and subdirectories:**
    ```bash
    python utils/cosmic-dust-bunny-collector/src/collector.py .
    ```

2.  **Dry run to find `.log` and `.bak` files older than 30 days in a specific project folder:**
    ```bash
    python utils/cosmic-dust-bunny-collector/src/collector.py /path/to/my/project --patterns '*.log' '*.bak' --age 30
    ```

3.  **Delete all `.tmp` files in `/var/tmp`:**
    ```bash
    python utils/cosmic-dust-bunny-collector/src/collector.py /var/tmp --patterns '*.tmp' --delete
    ```

4.  **Delete all files older than 7 days in the current directory, using default patterns:**
    ```bash
    python utils/cosmic-dust-bunny-collector/src/collector.py . --age 7 --delete
    ```

## Development

### Running Tests

```bash
python -m unittest utils/cosmic-dust-bunny-collector/tests/test_collector.py
```
