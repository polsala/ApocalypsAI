# Nightly Cosmic Dust Collector

## Description

The Nightly Cosmic Dust Collector is a whimsical-yet-useful utility designed to keep your digital cosmos tidy. It scans specified directories for 'cosmic dust' – old files, temporary artifacts, and forgotten logs – and helps you sweep them away. This prevents clutter, frees up disk space, and ensures your systems run smoothly without being bogged down by digital debris.

It supports filtering by file age and name patterns, and includes a crucial dry-run mode to preview deletions before they happen.

## Usage

```bash
python src/dust_collector.py <directory> --age <days> [--pattern <glob_pattern>] [--dry-run]
```

### Arguments:

*   `<directory>`: The path to the directory to scan for old files.
*   `--age <days>`: Files older than this many days will be considered for deletion.
*   `--pattern <glob_pattern>`: (Optional) Only files matching this glob pattern (e.g., `*.log`, `temp_*`) will be considered. If omitted, all files are considered.
*   `--dry-run`: (Optional) If present, the utility will only report which files *would* be deleted, without actually deleting them. Highly recommended for initial runs.

## Examples

1.  **Dry-run to see all files older than 30 days in `/var/log`:**
    ```bash
    python src/dust_collector.py /var/log --age 30 --dry-run
    ```

2.  **Delete `.tmp` files older than 7 days in `/tmp/my_app`:**
    ```bash
    python src/dust_collector.py /tmp/my_app --age 7 --pattern "*.tmp"
    ```

3.  **Delete all files older than 90 days in your downloads folder:**
    ```bash
    python src/dust_collector.py ~/Downloads --age 90
    ```

## Installation

This utility is self-contained and requires Python 3.6+ (tested with 3.11). No external dependencies are needed beyond the standard library.

Simply navigate to the `utils/nightly-cosmic-dust-collector` directory and run the `src/dust_collector.py` script.
