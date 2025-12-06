# Cataclysmic Cache Cleaner

## Overview

The Cataclysmic Cache Cleaner is a Python utility designed to help you prepare for any eventuality by identifying and reporting on old or excessively large files within specified directories. Think of it as a pre-apocalyptic system hygiene tool, helping you reclaim precious disk space by highlighting files that are likely safe to delete. It doesn't delete files itself, but provides a clear report for your review.

## Features

*   Scans multiple directories recursively.
*   Filters files based on a minimum age (in days).
*   Filters files based on a minimum size (in megabytes).
*   Generates a human-readable report of "cataclysmic candidates" for deletion.

## Usage

To run the cleaner, execute the `cleaner.py` script with the desired paths and criteria.

```bash
python src/cleaner.py --path /var/log --path ~/Downloads --min-age 30 --min-size 100
```

### Arguments

*   `--path <directory>`: (Required, can be specified multiple times) The directory to scan. The utility will recursively search this path.
*   `--min-age <days>`: (Optional, default: 30) Minimum age in days for a file to be considered a candidate. Files older than this will be flagged.
*   `--min-size <megabytes>`: (Optional, default: 50) Minimum size in megabytes for a file to be considered a candidate. Files larger than this will be flagged.

## Example Output

```
Cataclysmic Cache Cleaner Report (Thresholds: Age >= 30 days, Size >= 50 MB)
--------------------------------------------------------------------------

Scanning: /var/log
  - /var/log/old_app.log (Age: 95 days, Size: 120.5 MB) - Candidate!
  - /var/log/archive/backup.zip (Age: 180 days, Size: 500.2 MB) - Candidate!

Scanning: ~/Downloads
  - ~/Downloads/large_installer.dmg (Age: 45 days, Size: 300.1 MB) - Candidate!

--------------------------------------------------------------------------
Total Cataclysmic Candidates Found: 3
```

## Development

### Running Tests

To ensure the cleaner is ready for any digital apocalypse, run its self-contained tests:

```bash
python -m unittest tests/test_cleaner.py
```
