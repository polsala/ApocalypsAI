# Cosmic Cache Cleaner

## Overview

The `Cosmic Cache Cleaner` is your trusty digital janitor, designed to help you declutter your file system by identifying 'cosmic debris' – files that are old, unused, or simply redundant. It scans a specified directory and reports on files that meet certain criteria, allowing you to make informed decisions about what to keep and what to jettison into the digital void.

This utility is perfect for maintaining a lean and efficient 'cosmic cache', ensuring your valuable storage isn't consumed by forgotten relics.

## Features

- **Age-based Debris Detection**: Identifies files older than a specified number of days.
- **Duplicate Anomaly Scanner**: Pinpoints identical files (based on content hash) that are needlessly occupying space.
- **Simulation Mode**: Reports findings without making any changes, allowing for safe review.

## Usage

```bash
python src/cleaner.py --directory /path/to/scan [--days-old <N>] [--find-duplicates]
```

### Arguments:

- `--directory <path>`: The root directory to scan for cosmic debris. (Required)
- `--days-old <N>`: Report files older than `N` days. (Default: 90 days)
- `--find-duplicates`: Enable scanning for duplicate files based on content hash. (Optional)
- `--simulate`: (Default) Only report findings; do not perform any deletion. (Currently, only simulation is supported for safety).

## Examples

1.  **Find files older than 180 days in your 'archive' folder:**
    ```bash
    python src/cleaner.py --directory /home/user/archive --days-old 180
    ```

2.  **Scan your 'downloads' folder for duplicates:**
    ```bash
    python src/cleaner.py --directory /home/user/downloads --find-duplicates
    ```

3.  **Combine both: find old files (default 90 days) and duplicates in your 'temp' folder:**
    ```bash
    python src/cleaner.py --directory /var/tmp --find-duplicates
    ```

## Installation

This utility is self-contained and requires Python 3.11+. No external dependencies are strictly required beyond standard library modules.

```bash
cd utils/nightly-cosmic-cache-cleaner
python src/cleaner.py --help
```
