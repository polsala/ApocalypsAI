# Nightly Byte-Bloom Gardener

## Overview

The Nightly Byte-Bloom Gardener is a whimsical yet practical utility designed to help you manage your digital garden. It scans specified directories for 'byte-blooms' – files that are both significantly large and haven't been modified recently. These files often represent forgotten data, old backups, or temporary artifacts that consume valuable disk space.

By identifying these byte-blooms, the Gardener helps you decide whether to 'prune' them (delete), 'replant' them (move to archival storage), or simply review their necessity, ensuring your file system remains tidy and efficient.

## Features

*   **Configurable Thresholds**: Define what constitutes a 'large' file (in MB) and 'infrequently modified' (in days).
*   **Directory Scanning**: Recursively scans a specified root directory.
*   **Clear Reporting**: Outputs a list of identified byte-blooms with their size and last modification date.

## Usage

```bash
python src/gardener.py --path /path/to/scan --size-mb 100 --age-days 90
```

### Arguments:

*   `--path <directory>`: The root directory to start scanning from. (Required)
*   `--size-mb <integer>`: Minimum file size in megabytes to consider a 'byte-bloom'. (Default: 50 MB)
*   `--age-days <integer>`: Minimum age in days (since last modification) to consider a 'byte-bloom'. (Default: 60 days)

## Example Output

```
Scanning /my/project/data for byte-blooms (>= 100 MB, >= 90 days old)...

Found 3 byte-blooms:

- /my/project/data/old_backup/archive_2022.zip (Size: 1.2 GB, Modified: 2022-01-15)
- /my/project/data/logs/large_debug.log (Size: 250 MB, Modified: 2023-03-01)
- /my/project/data/temp/huge_export.csv (Size: 150 MB, Modified: 2023-02-20)

Consider pruning or replanting these forgotten byte-blooms to free up space!
```

## Installation

This utility is self-contained and requires Python 3.6+.

1.  Navigate to the `nightly-byte-bloom-gardener` directory.
2.  Run directly: `python src/gardener.py --help`

## Development & Testing

To run tests:

```bash
python -m unittest tests/test_gardener.py
```
