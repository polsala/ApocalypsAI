# Chronicle Keeper's Content Compressor

## Overview

In the post-apocalyptic digital wasteland, every byte counts! The Chronicle Keeper's Content Compressor is your trusty companion for decluttering your digital archives. It scans specified directories to identify redundant files (duplicates), excessively large files, and forgotten empty files, providing a clear report with actionable suggestions.

Keep your data lean, mean, and ready for the next data migration or storage crunch!

## Features

*   **Duplicate File Detection**: Identifies files with identical content using MD5 hashing.
*   **Large File Identification**: Flags files exceeding a configurable size threshold.
*   **Empty File Discovery**: Locates zero-byte files that are just taking up space.
*   **Comprehensive Report**: Generates a summary of findings with suggested actions.
*   **Non-Destructive**: By default, only reports findings. No files are modified or deleted without explicit user action.

## Installation

This utility is self-contained and written in Python 3.11+. No external dependencies are required beyond the standard library.

To run it, simply navigate to the `src` directory and execute the `compressor.py` script.

## Usage

```bash
python3 src/compressor.py --path <directory_to_scan> [--min-size <bytes>] [--report-only]
```

### Arguments

*   `--path <directory_to_scan>`: **Required**. The root directory to start scanning from.
*   `--min-size <bytes>`: Optional. The minimum size (in bytes) for a file to be considered 'large'. Defaults to `104857600` (100 MB).
*   `--report-only`: Optional. If present, the utility will only print the report and not attempt any interactive actions (though currently, no interactive actions are implemented, this flag is for future expansion).

### Example

Scan your 'archive' folder, flagging files larger than 50MB:

```bash
python3 src/compressor.py --path /home/user/archive --min-size 52428800
```

## Output

The utility will print a structured report to the console, detailing:

*   Total files scanned.
*   Total size scanned.
*   Lists of duplicate files (grouped by content hash).
*   Lists of large files.
*   Lists of empty files.

Each section will include suggested actions, such as 'Consider deleting duplicates' or 'Review and compress large files'.

## Development & Testing

Tests are located in the `tests/` directory and can be run using `pytest` or `python3 -m unittest`.

```bash
python3 -m unittest tests/test_compressor.py
```
