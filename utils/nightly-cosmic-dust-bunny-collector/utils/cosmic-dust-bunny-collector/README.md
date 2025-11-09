# Cosmic Dust Bunny Collector

## Overview

The `cosmic-dust-bunny-collector` is a delightful little utility designed to help you declutter your digital environment. It scans specified directories for files that haven't been modified in a long time (your 'cosmic dust bunnies') and provides options to report them or even remove them. Keep your file system sparkling clean and ready for any intergalactic event!

## Features

*   **Directory Scanning**: Recursively scans a target directory for files.
*   **Age-Based Filtering**: Identifies files older than a specified number of days.
*   **Dry Run Mode**: Preview which files would be affected without making any changes.
*   **Deletion Mode**: Safely remove identified 'dust bunnies' (use with caution!).

## Installation

This utility is self-contained and written in Python 3.11+. No special installation steps are required beyond having a compatible Python interpreter.

## Usage

Run the script from your terminal:

```bash
python3 utils/cosmic-dust-bunny-collector/src/dust_bunny_collector.py --path <directory_to_scan> [options]
```

### Arguments

*   `--path <directory>` (required): The root directory to start scanning for old files.
*   `--days-old <int>` (optional, default: 30): Files not modified within this many days will be considered 'dust bunnies'.
*   `--dry-run` (optional): If present, the utility will only report files that would be deleted, without actually deleting them. This is highly recommended for a first run.
*   `--delete` (optional): If present, the utility will actually delete the identified old files. **Use with extreme caution!** This option is ignored if `--dry-run` is also present.

### Examples

1.  **Find files older than 60 days in your downloads folder (dry run):**
    ```bash
    python3 utils/cosmic-dust-bunny-collector/src/dust_bunny_collector.py --path ~/Downloads --days-old 60 --dry-run
    ```

2.  **Actually delete files older than 90 days in a temporary directory:**
    ```bash
    python3 utils/cosmic-dust-bunny-collector/src/dust_bunny_collector.py --path /tmp/old_logs --days-old 90 --delete
    ```

3.  **Report all files older than the default 30 days in your documents folder:**
    ```bash
    python3 utils/cosmic-dust-bunny-collector/src/dust_bunny_collector.py --path ~/Documents
    ```

## Development

To run tests, navigate to the `utils/cosmic-dust-bunny-collector` directory and execute:

```bash
python3 -m unittest tests/test_dust_bunny_collector.py
```
