# Nightly Cosmic Dust Collector

## Overview

The Nightly Cosmic Dust Collector is a whimsical-yet-useful utility designed to help maintain a clean and tidy repository by identifying and managing 'cosmic dust' – small, forgotten, or empty files that accumulate over time. It scans specified directories for files that fall below a certain size threshold or are completely empty, offering options to simply list them, archive them to a designated location, or delete them outright.

Keeping your repository free of unnecessary clutter improves readability, reduces repository size, and can even speed up operations like cloning and indexing.

## Features

*   **Configurable Size Threshold**: Define what constitutes 'small' by setting a maximum file size in kilobytes.
*   **Empty File Detection**: Automatically identifies and flags empty files as dust.
*   **Dry Run Mode**: Preview which files would be affected without making any changes.
*   **Actionable Options**: Choose to list, archive, or delete identified dust files.

## Usage

```bash
python src/dust_collector.py --help
```

```bash
# List all files smaller than 1KB (or empty) in the current directory and its subdirectories
python src/dust_collector.py --path . --max-size 1 --action list

# Delete all files smaller than 500 bytes (or empty) in the 'logs/' directory
# WARNING: This will permanently delete files. Use with caution!
python src/dust_collector.py --path logs/ --max-size 0.5 --action delete

# Archive all files smaller than 2KB (or empty) in 'temp/' to an 'archive_dust/' directory
python src/dust_collector.py --path temp/ --max-size 2 --action archive --archive-dir archive_dust/

# Dry run: see what would be deleted if action was 'delete' for files < 1KB
python src/dust_collector.py --path . --max-size 1 --action delete --dry-run
```

## Installation

This utility is self-contained and requires Python 3.6+.

1.  Navigate to the `utils/nightly-cosmic-dust-collector/` directory.
2.  Run the `dust_collector.py` script directly.

## Development

To run tests:

```bash
python -m unittest tests/test_dust_collector.py
```
