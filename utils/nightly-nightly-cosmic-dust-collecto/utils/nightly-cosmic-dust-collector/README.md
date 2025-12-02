# Nightly Cosmic Dust Collector

## Overview

The Nightly Cosmic Dust Collector is a whimsical-yet-useful utility designed to help maintain a tidy repository by identifying and optionally quarantining small, forgotten, or empty files that might accumulate over time. Think of it as a digital vacuum cleaner for your project's nooks and crannies.

It scans a specified directory, looking for files that fall below a certain size threshold or are completely empty. These files, deemed 'cosmic dust,' are then reported, giving you an overview of potential clutter. For more proactive cleanup, the utility can also move these files to a designated 'quarantine' directory, allowing for later review or deletion.

## Features

*   **Directory Scanning**: Recursively scans a target directory.
*   **Size Thresholding**: Identifies files smaller than a configurable byte size.
*   **Empty File Detection**: Specifically flags empty files.
*   **Reporting**: Outputs a list of identified 'dust' files with their sizes.
*   **Quarantine Functionality**: Optionally moves identified files to a specified quarantine directory instead of deleting them directly, providing a safety net and preserving the original directory structure.

## Usage

```bash
python src/dust_collector.py <target_directory> [--max-size <bytes>] [--quarantine-dir <path>]
```

**Arguments:**

*   `<target_directory>`: The root directory to start scanning for cosmic dust.
*   `--max-size <bytes>`: (Optional) The maximum file size (in bytes) to consider as 'cosmic dust'. Files smaller than or equal to this size will be flagged. Defaults to `1024` bytes (1KB).
*   `--quarantine-dir <path>`: (Optional) If provided, identified files will be moved to this directory. If not provided, files will only be reported.

**Examples:**

Scan the current directory for files up to 500 bytes and report them:
```bash
python src/dust_collector.py . --max-size 500
```

Scan the 'logs' directory for files up to 1KB and move them to a 'quarantine_zone' folder:
```bash
python src/dust_collector.py logs --max-size 1024 --quarantine-dir ./quarantine_zone
```

## Development

To run tests:

```bash
python -m unittest tests/test_dust_collector.py
```
