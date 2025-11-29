# Nightly Cosmic Dust Collector

## Overview

The Nightly Cosmic Dust Collector is a whimsical-yet-useful utility designed to help you maintain a tidy digital environment. It scans a specified directory for files that are older than a configurable number of days and, optionally, removes them. Think of it as a diligent space janitor, sweeping away the accumulated "cosmic dust" of old logs, temporary files, or forgotten backups.

## Features

*   **Age-based Deletion**: Identify and remove files older than a specified threshold.
*   **Dry Run Mode**: Preview which files would be deleted without actually removing them.
*   **Recursive Scan**: Optionally scan subdirectories for dust.

## Usage

### Prerequisites

*   Python 3.6+ (tested with 3.11)

### Running the Collector

Navigate to the `src` directory and run the `dust_collector.py` script.

```bash
python src/dust_collector.py --path /path/to/your/directory --days 30 [--dry-run] [--recursive] [--verbose]
```

### Arguments

*   `--path <directory>` (required): The directory to scan for old files.
*   `--days <integer>` (required): Files older than this many days will be considered "dust".
*   `--dry-run`: If present, the utility will only list files that *would* be deleted, without actually deleting them.
*   `--recursive`: If present, the utility will scan subdirectories as well.
*   `--verbose`: If present, print more detailed output about files being processed.

### Examples

1.  **List files older than 60 days in `/var/log/app` (dry run):**
    ```bash
    python src/dust_collector.py --path /var/log/app --days 60 --dry-run
    ```

2.  **Delete files older than 7 days in `/tmp/backups` (recursive):**
    ```bash
    python src/dust_collector.py --path /tmp/backups --days 7 --recursive
    ```

3.  **Delete files older than 30 days in the current directory:**
    ```bash
    python src/dust_collector.py --path . --days 30
    ```
