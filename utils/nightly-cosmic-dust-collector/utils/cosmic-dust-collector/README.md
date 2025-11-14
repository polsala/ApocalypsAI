# Cosmic Dust Collector

## Overview

The 'Cosmic Dust Collector' is a whimsical yet highly practical utility designed to help you maintain digital hygiene in your critical systems. Over time, files accumulate – logs, temporary data, forgotten backups – becoming 'cosmic dust' that clogs your storage and obscures important information. This tool helps you identify and optionally purge these ancient artifacts, ensuring your directories remain pristine and ready for the next cosmic event.

## Features

*   **Age-based Filtering**: Specify a threshold (in days) to identify files older than a certain age.
*   **Dry Run Mode**: Safely preview which files would be affected before committing to deletion.
*   **Recursive Scanning**: Scans subdirectories to ensure no dust bunny is left unturned.
*   **Whimsical Output**: Provides clear, concise, and slightly dramatic feedback on its operations.

## Installation

This utility is self-contained and written in Python 3.11+. No external dependencies are required beyond the standard library.

To use it, simply navigate to the `utils/cosmic-dust-collector/` directory.

## Usage

```bash
python src/dust_collector.py <directory_path> [--age <days>] [--delete]
```

### Arguments:

*   `<directory_path>`: The path to the directory you wish to clean.
*   `--age <days>`: (Optional) The minimum age in days for a file to be considered 'cosmic dust'. Files older than this will be targeted. Defaults to 30 days.
*   `--delete`: (Optional) If present, the utility will actually delete the identified files. **Use with caution!** By default, it runs in dry-run mode, only listing files.

### Examples:

List files older than 60 days in `/var/log/apocalypse`:
```bash
python src/dust_collector.py /var/log/apocalypse --age 60
```

Delete files older than 7 days in `/tmp/preparations`:
```bash
python src/dust_collector.py /tmp/preparations --age 7 --delete
```

## Development & Testing

To run tests, navigate to the `utils/cosmic-dust-collector/` directory and execute:

```bash
python -m unittest tests/test_dust_collector.py
```

Tests are designed to be deterministic and offline, using temporary directories and mocked file system operations to ensure reliability without affecting your actual files.
