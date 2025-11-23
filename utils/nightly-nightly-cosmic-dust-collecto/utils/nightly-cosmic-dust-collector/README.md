# Nightly Cosmic Dust Collector

## Overview

The Nightly Cosmic Dust Collector is a whimsical-yet-useful utility designed to help maintain a tidy project directory by identifying and optionally archiving 'cosmic dust' – small, forgotten, or temporary files that accumulate over time. It helps declutter your workspace, making it easier to navigate and manage your files.

## Features

*   **Scans for Empty Files**: Identifies files with zero bytes.
*   **Detects Tiny Files**: Finds files smaller than a configurable size threshold (default: 1KB).
*   **Locates Old Temporary Files**: Pinpoints files matching common temporary patterns (e.g., `.tmp`, `~`, `#`) that haven't been modified in a configurable number of days (default: 30 days).
*   **Dry Run Mode**: Preview which files would be affected without making any changes.
*   **Archiving**: Move identified 'dust' files to a specified 'cosmic dustbin' directory.
*   **Recursive Scanning**: Traverses subdirectories to ensure thorough cleaning.

## Usage

```bash
python src/dust_collector.py --target-dir /path/to/project --dustbin-dir /path/to/dustbin
```

### Command-line Arguments

*   `--target-dir <path>` (required): The directory to scan for cosmic dust.
*   `--dustbin-dir <path>` (required): The directory where collected dust will be moved. This directory will be created if it doesn't exist.
*   `--max-size-kb <int>` (optional, default: 1): Maximum file size in kilobytes to consider as 'dust'. Files larger than this will be ignored unless they are empty or old temporary files.
*   `--max-age-days <int>` (optional, default: 30): Minimum age in days for temporary files to be considered 'dust'.
*   `--temp-patterns <str>` (optional, default: '.tmp,~,#,.bak,.log'): Comma-separated list of file extensions or patterns to identify temporary files.
*   `--dry-run` (optional): If set, the utility will only list files that would be collected, without moving them. This is the default behavior if `--move` is not specified.
*   `--move` (optional): If set, the utility will actually move the identified files to the dustbin directory. **Use with caution!**

### Example: Dry Run

```bash
python src/dust_collector.py --target-dir ./my_project --dustbin-dir ./cosmic_dust --dry-run
```

This will print a list of files that would be moved without actually moving them.

### Example: Move Files

```bash
python src/dust_collector.py --target-dir ./my_project --dustbin-dir ./cosmic_dust --move --max-size-kb 5 --max-age-days 60
```

This will move empty files, files smaller than 5KB, and temporary files older than 60 days from `my_project` to `cosmic_dust`.

## Development

### Running Tests

To run the tests for the Cosmic Dust Collector, navigate to the `utils/nightly-cosmic-dust-collector` directory and execute:

```bash
pip install pytest
pytest tests/
```
