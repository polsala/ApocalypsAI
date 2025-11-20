# Nightly Cache Cleaner

## Overview

The `nightly-cache-cleaner` is a vigilant digital scavenger designed to help you reclaim precious disk space by identifying and optionally removing old, forgotten files. In the chaotic aftermath, every byte counts! This utility scans specified directories for files that haven't been modified in a configurable number of days and provides a summary, with an option to perform a 'dry run' or proceed with actual deletion.

## Usage

```bash
python src/cleaner.py --path /path/to/scan --days 30 [--delete]
```

### Arguments:

*   `--path <directory>`: The root directory to start scanning from. Required.
*   `--days <int>`: The age threshold in days. Files older than this will be flagged. Required.
*   `--delete`: (Optional) If provided, the utility will actually delete the identified files. Without this flag, it performs a dry run and only lists files.

## Example Dry Run

```bash
python src/cleaner.py --path /var/log --days 90
```

This will list all files in `/var/log` (and its subdirectories) that are older than 90 days, without deleting them.

## Example Deletion

```bash
python src/cleaner.py --path ~/Downloads --days 180 --delete
```

This will delete all files in `~/Downloads` (and its subdirectories) that are older than 180 days.

## Development

To run tests:

```bash
python -m unittest tests/test_cleaner.py
```
