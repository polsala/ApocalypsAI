# Cosmic Dust Collector

## Sweep Away Digital Detritus

The `cosmic-dust-collector` is a whimsical yet practical utility designed to help you maintain a pristine digital environment by identifying and optionally removing 'digital dust' – old, large, or specific types of files that clutter your file system.

Think of it as a tiny, automated janitor for your directories, ensuring only the freshest and most vital data remains.

## Features

*   **Age-based filtering**: Find files older than a specified number of days.
*   **Size-based filtering**: Locate files larger than a certain megabyte threshold.
*   **Extension-based filtering**: Target specific file types (e.g., `.log`, `.tmp`, `.bak`).
*   **Dry Run Mode**: Preview what would be cleaned without making any changes.
*   **Recursive Scanning**: Traverses subdirectories to find hidden dust.

## Usage

To run the Cosmic Dust Collector, navigate to its directory and execute the `collector.py` script. It accepts several command-line arguments:

```bash
python3 src/collector.py <path> [--min-age-days <days>] [--min-size-mb <mb>] [--extensions <ext1,ext2,...>] [--dry-run]
```

### Arguments:

*   `<path>`: The root directory to start scanning from. (Required)
*   `--min-age-days <days>`: Only consider files older than this many days. (Optional, default: 30)
*   `--min-size-mb <mb>`: Only consider files larger than this many megabytes. (Optional, default: 10)
*   `--extensions <ext1,ext2,...>`: Comma-separated list of file extensions to target (e.g., `log,tmp,bak`). (Optional)
*   `--dry-run`: If present, the utility will only report files to be cleaned, without actually deleting them. (Optional)

## Examples

1.  **Find all files older than 60 days in `/var/log` (dry run):**
    ```bash
    python3 src/collector.py /var/log --min-age-days 60 --dry-run
    ```

2.  **Delete all `.tmp` and `.bak` files larger than 50MB in your home directory:**
    ```bash
    python3 src/collector.py ~/ --min-size-mb 50 --extensions tmp,bak
    ```

3.  **Identify all files older than 7 days and larger than 1MB in the current directory:**
    ```bash
    python3 src/collector.py . --min-age-days 7 --min-size-mb 1 --dry-run
    ```

## Installation

This utility is self-contained and requires Python 3.6+.

```bash
cd utils/cosmic-dust-collector
python3 src/collector.py --help
```
