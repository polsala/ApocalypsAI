# Nightly Cosmic Dust Collector

## Purpose

The Nightly Cosmic Dust Collector is a whimsical-yet-useful utility designed to help maintain a clean and tidy repository or filesystem. It scans specified directories for files that might be considered 'cosmic dust' – files that are empty, unusually small, or very old. By identifying these files, it helps users review and potentially remove forgotten artifacts, temporary files, or remnants that no longer serve a purpose, thus reducing clutter and improving overall system hygiene.

## Features

*   **Empty File Detection**: Identifies files with zero bytes.
*   **Small File Detection**: Flags files smaller than a configurable size threshold (excluding empty files).
*   **Old File Detection**: Highlights files that haven't been modified for a configurable duration.
*   **Recursive Scanning**: Traverses directories to find dust deep within.
*   **Report Generation**: Outputs a list of identified 'dust' files with their properties.

## Usage

```bash
python src/collector.py <directory_path> [--max-size <bytes>] [--max-age <days>]
```

### Arguments:

*   `<directory_path>`: The root directory to start scanning from.
*   `--max-size <bytes>`: (Optional) Maximum file size in bytes to consider a file 'small'. Default: `1024` (1KB).
*   `--max-age <days>`: (Optional) Maximum age in days (since last modification) to consider a file 'old'. Default: `90` days.

### Examples:

Scan the current directory for dust files (empty, <1KB, or >90 days old):
```bash
python src/collector.py .
```

Scan a specific directory, considering files under 500 bytes or older than 30 days as dust:
```bash
python src/collector.py /path/to/my/project --max-size 500 --max-age 30
```

## Installation

This utility is self-contained and requires no special installation beyond a Python 3.11+ environment.

```bash
cd utils/nightly-cosmic-dust-collector
python src/collector.py .
```

## Development & Testing

To run the tests:

```bash
cd utils/nightly-cosmic-dust-collector
python -m unittest tests/test_collector.py
```
