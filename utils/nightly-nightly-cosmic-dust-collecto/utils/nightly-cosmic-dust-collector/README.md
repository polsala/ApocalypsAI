# Nightly Cosmic Dust Collector

## Overview

The Nightly Cosmic Dust Collector is a vital utility for maintaining digital hygiene in the ApocalypsAI repository. It helps clear out accumulated 'cosmic dust' – old, temporary, or unwanted files and directories – based on age and configurable patterns. Think of it as a digital broom, sweeping away the detritus of past operations to keep your systems lean and efficient.

## Features

*   **Age-based Cleanup**: Target files and directories older than a specified number of days.
*   **Pattern Matching**: Use glob patterns (e.g., `*.log`, `cache_*`) to precisely identify what to clean.
*   **Dry Run Mode**: Preview what would be deleted without actually removing anything.
*   **Verbose Output**: Get detailed logs of the cleaning process.
*   **Self-contained**: No external dependencies beyond standard Python libraries.

## Usage

```bash
python src/dust_collector.py --path /path/to/scan --age 7 --patterns "*.log" "temp_*" --dry-run
```

### Arguments

*   `--path <directory>`: The root directory to scan for cosmic dust. (Required)
*   `--age <days>`: Files/directories older than this many days will be considered for deletion. (Default: 30)
*   `--patterns <pattern1> <pattern2> ...`: One or more glob patterns to match against file/directory names. If not provided, all files/directories older than `--age` are considered. (Optional)
*   `--dry-run`: If set, the utility will only report what *would* be deleted, without performing any actual deletions. (Optional)
*   `--verbose`: If set, provides more detailed output about the scanning and deletion process. (Optional)

## Examples

*   **Clean all `.tmp` files older than 14 days in the current directory (dry run):**
    ```bash
    python src/dust_collector.py --path . --age 14 --patterns "*.tmp" --dry-run
    ```
*   **Delete all directories starting with `cache_` older than 30 days in `/var/log/`:**
    ```bash
    python src/dust_collector.py --path /var/log --age 30 --patterns "cache_*" 
    ```
*   **List all files/directories older than 60 days in `/tmp` (dry run, verbose):**
    ```bash
    python src/dust_collector.py --path /tmp --age 60 --dry-run --verbose
    ```

## Development

To run tests:

```bash
python -m unittest tests/test_dust_collector.py
```
