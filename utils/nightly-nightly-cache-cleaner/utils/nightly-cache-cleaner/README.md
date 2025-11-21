# Nightly Cache Cleaner: The Digital Dust Bunny Exterminator

## Overview

In the post-apocalyptic digital landscape, forgotten files accumulate like radioactive dust, silently consuming precious disk space. The **Nightly Cache Cleaner** is your trusty utility to identify and optionally purge these digital dust bunnies, ensuring your systems remain lean and efficient. It scans specified directories for old, large, or temporary files based on configurable criteria, offering both a safe dry-run mode and a decisive deletion mode.

## Features

*   **Targeted Scanning**: Define specific directories to scan for clutter.
*   **Age-Based Filtering**: Identify files older than a specified number of days.
*   **Size-Based Filtering**: Pinpoint files larger than a certain megabyte threshold.
*   **Pattern Matching**: Include or exclude files based on glob patterns (e.g., `*.log`, `temp_*`).
*   **Dry Run Mode**: Safely preview which files would be deleted without making any changes.
*   **Deletion Mode**: Confidently remove identified files to reclaim disk space.

## Installation

This utility is self-contained and written in Python 3.11. No external dependencies are strictly required beyond the standard library.

To run it, simply navigate to its directory and execute the `cleaner.py` script.

## Usage

```bash
python src/cleaner.py --help
```

### Basic Scan (Dry Run)

Scan `/tmp` and `~/Downloads` for files older than 30 days and larger than 10MB, without deleting anything:

```bash
python src/cleaner.py \
    --paths /tmp ~/Downloads \
    --max-age-days 30 \
    --min-size-mb 10 \
    --dry-run
```

### Deleting Specific File Types

Scan `/var/log` for `.log` files older than 7 days and delete them:

```bash
python src/cleaner.py \
    --paths /var/log \
    --max-age-days 7 \
    --include-patterns "*.log" \
    --delete
```

### Excluding Patterns

Scan a project directory, deleting old build artifacts but preserving `.git` files:

```bash
python src/cleaner.py \
    --paths /path/to/my/project \
    --max-age-days 60 \
    --include-patterns "build/*" "dist/*" \
    --exclude-patterns ".git/*" \
    --delete
```

### Arguments

*   `--paths <path> [<path> ...]`: One or more directories to scan. Required.
*   `--max-age-days <int>`: Files older than this many days will be considered. Default: `None` (no age filter).
*   `--min-size-mb <int>`: Files larger than this many megabytes will be considered. Default: `None` (no size filter).
*   `--include-patterns <pattern> [<pattern> ...]`: Glob patterns for files to include (e.g., `*.tmp`, `cache/*`). Default: `None` (all files).
*   `--exclude-patterns <pattern> [<pattern> ...]`: Glob patterns for files to exclude (e.g., `*.important`, `config/*`). Default: `None` (no exclusions).
*   `--dry-run`: Perform a dry run, listing files that *would* be deleted without actually deleting them. This is the default behavior if `--delete` is not specified.
*   `--delete`: Actually delete the identified files. **Use with caution!**

## Development

To contribute or extend this utility, ensure you have Python 3.11 installed.
Run tests using `pytest` (install `pytest` if you don't have it: `pip install pytest`).

```bash
pytest tests/
```
