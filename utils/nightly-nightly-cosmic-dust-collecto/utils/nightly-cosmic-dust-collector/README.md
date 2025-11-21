# Nightly Cosmic Dust Collector

## Overview

The Nightly Cosmic Dust Collector is a whimsical-yet-useful utility designed to help keep your project directories clean and tidy. It scans a specified directory for files of certain types (e.g., log files, temporary files, backup files) that are older than a defined age threshold, and then moves them into an `archive/` subdirectory. This helps prevent clutter and ensures that only relevant, recent files remain in your active workspace.

## Features

*   **Targeted Cleanup**: Specify file extensions to target (e.g., `.log`, `.tmp`, `.bak`).
*   **Age-Based Archiving**: Only files older than a configurable number of days are moved.
*   **Non-Destructive**: Files are moved to an `archive/` folder, not deleted, allowing for review if needed.
*   **Recursive Scanning**: Scans subdirectories within the specified path.

## Usage

```bash
python src/dust_collector.py --directory /path/to/your/project --age 30 --extensions log tmp
```

### Arguments:

*   `--directory` (required): The root directory to scan for old files.
*   `--age` (required): The age threshold in days. Files older than this will be archived.
*   `--extensions` (required): A space-separated list of file extensions (without the leading dot) to target for archiving. Example: `log tmp bak`.
*   `--dry-run` (optional): If specified, the utility will only report what *would* be moved, without actually moving any files.

## Example

To archive all `.log` and `.tmp` files in the current directory that are older than 60 days:

```bash
python src/dust_collector.py --directory . --age 60 --extensions log tmp
```

## Installation

This utility is self-contained and requires no external dependencies beyond standard Python 3.11+ libraries. Simply place the `nightly-cosmic-dust-collector` folder in your `utils/` directory.

## Development

To run tests:

```bash
python -m unittest tests/test_dust_collector.py
```
