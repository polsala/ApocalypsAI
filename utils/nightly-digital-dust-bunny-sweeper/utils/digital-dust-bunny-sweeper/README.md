# Digital Dust Bunny Sweeper

## Overview
The Digital Dust Bunny Sweeper is a whimsical yet practical utility designed to help you identify and manage "digital dust bunnies" within your file systems. These are typically files that are either excessively large, consuming valuable disk space, or files that haven't been touched in a very long time, potentially indicating forgotten or unused assets.

This tool provides a report, allowing you to decide which files to clean up, archive, or simply acknowledge. It *never* deletes or modifies any files.

## Features
- Scans a specified directory recursively.
- Identifies files larger than a configurable size threshold.
- Identifies files older than a configurable age threshold (based on last modification time).
- Outputs a clear, human-readable report.

## Installation
This utility is self-contained and written in Python 3.11+. No special installation steps are required beyond having Python installed.

## Usage

```bash
python src/sweeper.py <directory_path> [--min-size-mb <MB>] [--min-age-days <DAYS>]
```

### Arguments:
- `<directory_path>`: The path to the directory you want to scan.
- `--min-size-mb <MB>`: (Optional) Report files larger than this size in megabytes. Default is 100 MB.
- `--min-age-days <DAYS>`: (Optional) Report files whose last modification date is older than this many days. Default is 365 days.

### Examples:
Scan the current directory for files larger than 50MB:
```bash
python src/sweeper.py . --min-size-mb 50
```

Scan `/var/log` for files older than 90 days:
```bash
python src/sweeper.py /var/log --min-age-days 90
```

Scan your home directory for files larger than 1GB or older than 2 years:
```bash
python src/sweeper.py ~/ --min-size-mb 1024 --min-age-days 730
```

## Output Example

```
Scanning directory: /path/to/your/project
Thresholds: Min Size = 100.0 MB, Min Age = 365 days

--- Digital Dust Bunnies Report ---

Large Files (>= 100.0 MB):
- /path/to/your/project/assets/large_video.mp4 (Size: 150.2 MB, Modified: 2023-01-15)
- /path/to/your/project/backup/old_archive.zip (Size: 250.8 MB, Modified: 2022-11-01)

Ancient Files (Modified >= 365 days ago):
- /path/to/your/project/docs/old_spec.pdf (Size: 2.1 MB, Modified: 2021-05-20)
- /path/to/your/project/src/legacy_code.py (Size: 0.5 MB, Modified: 2020-03-10)

No dust bunnies found matching criteria.
```
