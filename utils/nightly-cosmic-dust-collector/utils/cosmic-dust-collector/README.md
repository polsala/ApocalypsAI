# Cosmic Dust Collector

## Overview

The `Cosmic Dust Collector` is a whimsical yet practical utility designed to help you maintain clean and tidy project directories. It scans a specified path for 'cosmic dust' – files that are old, temporary, or match specific patterns – and provides options to list them (dry run) or delete them.

Think of it as a digital broom for your repository, sweeping away the forgotten artifacts of past development cycles.

## Features

*   **Age-based cleanup**: Identify and mark files older than a specified number of days.
*   **Pattern-based cleanup**: Target files by name patterns (e.g., `*.log`, `*.tmp`, `backup.bak`).
*   **Dry Run Mode**: Preview which files would be deleted without making any actual changes.
*   **Recursive Scanning**: Scans all subdirectories within the specified path.

## Installation

This utility is self-contained and written in Python 3.11+. No special installation steps or external dependencies are required beyond a standard Python environment.

## Usage

Navigate to the `utils/cosmic-dust-collector/` directory and run the `dust_collector.py` script.

```bash
python src/dust_collector.py <path_to_scan> [--dry-run] [--age-days <days>] [--patterns <pattern1,pattern2,...>]
```

### Arguments

*   `<path_to_scan>`: The root directory where the Cosmic Dust Collector will begin its scan.
*   `--dry-run`: (Optional) If present, the utility will only list the files it *would* delete, without actually removing them. Highly recommended for initial runs.
*   `--age-days <days>`: (Optional) An integer specifying that files older than this many days should be considered 'dust'. If 0 (default), no age-based filtering is applied.
*   `--patterns <pattern1,pattern2,...>`: (Optional) A comma-separated list of file name patterns (e.g., `*.log`, `*.tmp`, `my_old_file.txt`). Files matching any of these patterns will be considered 'dust'. Uses `fnmatch` for pattern matching (e.g., `*` for wildcards).

### Examples

1.  **List all `.log` and `.tmp` files in the current directory and its subdirectories (dry run):**
    ```bash
    python src/dust_collector.py . --dry-run --patterns "*.log,*.tmp"
    ```

2.  **Delete all files older than 30 days in `/var/log/my_app`:**
    ```bash
    python src/dust_collector.py /var/log/my_app --age-days 30
    ```

3.  **List all `.bak` files and files older than 7 days in your home directory:**
    ```bash
    python src/dust_collector.py ~/my_project --dry-run --age-days 7 --patterns "*.bak"
    ```

4.  **Delete a specific old file:**
    ```bash
    python src/dust_collector.py . --patterns "legacy_config.old"
    ```

## Development & Testing

To run the automated tests for the Cosmic Dust Collector, navigate to the `utils/cosmic-dust-collector/` directory and execute:

```bash
python -m unittest tests/test_dust_collector.py
```
