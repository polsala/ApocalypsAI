# Nightly Cosmic Dust Collector

## Overview

The Nightly Cosmic Dust Collector is a utility designed to help maintain a clean and efficient repository by identifying and managing old or temporary files. Like a diligent cosmic janitor, it sweeps through your specified directories, collecting 'dust' – files that match certain patterns and are older than a defined age threshold. It can then list these files, delete them, or move them to a dedicated archive.

## Features

*   **Targeted Scanning**: Specify a root directory to scan.
*   **Age-Based Filtering**: Only consider files older than a configurable number of days.
*   **Pattern Matching**: Filter files by glob patterns (e.g., `*.log`, `temp_*`, `*.bak`).
*   **Multiple Actions**: Choose to `list` (default), `delete`, or `archive` the identified files.
*   **Archiving**: Moves old files to a `.dust_archive` subdirectory within the scanned directory, providing a safety net before permanent deletion.

## Usage

```bash
python src/dust_collector.py --path <directory> [--age-days <days>] [--patterns <pattern1> <pattern2> ...] [--action <list|delete|archive>]
```

### Arguments:

*   `--path <directory>`: The root directory to scan for old files. (Required)
*   `--age-days <days>`: Files older than this many days will be considered 'dust'. Default is `30`. (Optional)
*   `--patterns <pattern1> <pattern2> ...`: One or more glob patterns to match file names (e.g., `*.log`, `*.tmp`, `backup_*`). Default is `['*.log', '*.tmp', '*.bak', '*.swp', '*~']`. (Optional)
*   `--action <list|delete|archive>`: The action to perform on identified files. `list` will print them, `delete` will remove them permanently, `archive` will move them to a `.dust_archive` folder. Default is `list`. (Optional)

## Examples

*   **List all `.log` files older than 60 days in the current directory:**
    ```bash
    python src/dust_collector.py --path . --age-days 60 --patterns "*.log"
    ```
*   **Delete all `.tmp` and `.bak` files older than 7 days in `/var/log/app`:**
    ```bash
    python src/dust_collector.py --path /var/log/app --age-days 7 --patterns "*.tmp" "*.bak" --action delete
    ```
*   **Archive all default 'dust' files older than 90 days in your home directory:**
    ```bash
    python src/dust_collector.py --path ~/ --age-days 90 --action archive
    ```

## Development

To run tests:

```bash
python -m unittest tests/test_dust_collector.py
```
