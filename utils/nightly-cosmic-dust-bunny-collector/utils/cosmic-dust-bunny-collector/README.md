# Cosmic Dust Bunny Collector

## Overview

In the vast expanse of your digital universe, tiny, forgotten files accumulate like cosmic dust bunnies, silently consuming precious space and cluttering your directories. The **Cosmic Dust Bunny Collector** is here to help!

This whimsical utility scans specified directories to identify these 'Cosmic Dust Bunnies' – files that are old, small, and likely no longer needed. It provides a clear report of these digital specks and offers options to safely quarantine them for review or, with caution, permanently remove them.

Keep your digital space pristine and free from interdimensional clutter!

## Features

*   **Scan Directories**: Recursively searches a target directory for files.
*   **Identify Dust Bunnies**: Flags files based on age (last modified) and size thresholds.
*   **Report**: Lists identified dust bunnies with their paths, sizes, and last modified dates.
*   **Quarantine**: Safely moves identified files to a designated 'quarantine' directory for manual review.
*   **Delete (Optional)**: Provides an option to permanently delete files (use with extreme caution).

## Installation

This utility is self-contained and written in Python 3.11. No external dependencies are required beyond the standard library.

1.  Navigate to the `utils/cosmic-dust-bunny-collector/` directory.
2.  Ensure you have Python 3.11 or newer installed.

## Usage

```bash
python src/dust_collector.py --help
```

### Basic Scan (List Dust Bunnies)

To simply list files older than 90 days and smaller than 1KB in the current directory:

```bash
python src/dust_collector.py --path . --age-days 90 --max-size-kb 1
```

### Quarantine Dust Bunnies

To move identified dust bunnies to a `quarantine_zone` directory (which will be created if it doesn't exist):

```bash
python src/dust_collector.py --path /path/to/scan --age-days 180 --max-size-kb 5 --quarantine /path/to/quarantine_zone
```

### Delete Dust Bunnies (Use with Extreme Caution!)

To permanently delete identified dust bunnies:

```bash
python src/dust_collector.py --path /path/to/scan --age-days 365 --max-size-kb 10 --delete
```

**Always review the list of files before performing any deletion or quarantine operation.**

## Configuration Options

*   `--path <directory>`: The directory to scan. Defaults to the current working directory.
*   `--age-days <int>`: Files older than this many days (based on last modification time) are considered dust bunnies. Default: 90.
*   `--max-size-kb <int>`: Files smaller than or equal to this size in kilobytes are considered dust bunnies. Default: 1 (1KB).
*   `--quarantine <directory>`: If provided, identified dust bunnies will be moved to this directory. The directory will be created if it doesn't exist.
*   `--delete`: If provided, identified dust bunnies will be permanently deleted. **This action is irreversible.**
*   `--verbose`: Print more detailed output during scanning.

## Development & Testing

To run the tests:

```bash
python -m unittest tests/test_dust_collector.py
```
