# Nightly Resource Reclaimer

## Overview

The 'Nightly Resource Reclaimer' is a vital utility for maintaining digital hygiene in a world where every byte counts. It scans a specified directory for two common forms of digital clutter: duplicate files (based on their content) and empty directories. By identifying these, it helps users understand where storage space can be reclaimed and organization improved.

## Features

*   **Duplicate File Detection**: Scans for files with identical content, regardless of their name or location.
*   **Empty Directory Identification**: Pinpoints directories that contain no files or subdirectories.
*   **Comprehensive Reporting**: Generates a clear, human-readable report detailing all identified issues.

## Usage

To run the Reclaimer, navigate to its directory and execute the `reclaimer.py` script with the target path:

```bash
python src/reclaimer.py /path/to/scan
```

Replace `/path/to/scan` with the actual directory you wish to analyze.

## Example Output

```
Scanning /home/user/data...

--- Duplicate Files Found ---

Group 1 (MD5: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6):
  - /home/user/data/documents/report_v1.txt (10 KB)
  - /home/user/data/backups/old_report.txt (10 KB)

Group 2 (MD5: f1e2d3c4b5a6f7e8d9c0b1a2f3e4d5c6):
  - /home/user/data/images/logo.png (50 KB)
  - /home/user/data/assets/brand/logo_copy.png (50 KB)

--- Empty Directories Found ---

  - /home/user/data/temp/
  - /home/user/data/empty_folder/sub_empty/

Scan complete. Reclaimed potential: 60 KB (from duplicates) + 2 empty directories.
```

## Development

This utility is written in Python 3.11+ and is self-contained. No external dependencies are required beyond the standard library.

### Running Tests

To ensure the Reclaimer is functioning correctly, run the provided tests:

```bash
python -m unittest tests/test_reclaimer.py
```
