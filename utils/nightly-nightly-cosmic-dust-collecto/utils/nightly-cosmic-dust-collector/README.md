# Nightly Cosmic Dust Collector

## Overview

The Nightly Cosmic Dust Collector is a whimsical-yet-useful utility designed to help you declutter your digital workspace. It scans specified directories for 'cosmic dust' – files that are either empty, very small, or haven't been touched in a long time. Once identified, these files can be listed, or optionally moved to a designated 'quarantine' directory for review, preventing them from accumulating and obscuring more important data.

Think of it as a tiny, automated janitor for your file system, sweeping away the digital debris that accumulates over time.

## Features

*   **Scan Directories**: Recursively scans one or more specified directories.
*   **Identify Dust**: Flags files based on configurable criteria:
    *   **Empty files**: Files with 0 bytes.
    *   **Small files**: Files below a specified size threshold (e.g., 1KB).
    *   **Old files**: Files not modified for a specified number of days.
*   **Quarantine Option**: Move identified 'dust' files to a separate quarantine directory instead of deleting them directly, allowing for manual review.
*   **Exclusion Patterns**: Ignore specific files or directories using glob patterns.

## Usage

```bash
python src/dust_collector.py --help
```

### Basic Scan (list only)

To scan a directory and list potential 'dust' files without moving them:

```bash
python src/dust_collector.py /path/to/scan --min-age 30 --max-size 1 --empty
```

This will list files in `/path/to/scan` that are older than 30 days, smaller than 1KB, or empty.

### Quarantine Dust

To move identified 'dust' files to a quarantine directory:

```bash
python src/dust_collector.py /path/to/scan --min-age 30 --max-size 1 --empty --quarantine /path/to/quarantine_zone
```

Files matching the criteria will be moved to `/path/to/quarantine_zone`. If the quarantine directory doesn't exist, it will be created.

### Ignoring Paths

To ignore specific files or directories (e.g., `.git` folders or `*.log` files):

```bash
python src/dust_collector.py /path/to/scan --ignore '.git/*' '*.log' --min-age 7
```

## Installation

This utility is self-contained and requires Python 3.6+.

1.  Navigate to the `utils/nightly-cosmic-dust-collector` directory.
2.  Run the `src/dust_collector.py` script directly.

## Development

To run tests:

```bash
python -m unittest tests/test_dust_collector.py
```
