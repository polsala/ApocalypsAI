# Cosmic Dust Bunny Collector

## Overview

The `cosmic-dust-bunny-collector` is a whimsical-yet-useful utility designed to help you keep your digital spaces tidy. It scans specified directories for 'dust bunnies' – digital remnants that accumulate over time, such as empty folders, old log files, and temporary files. By identifying these, it helps you maintain a cleaner, more organized repository or system.

## Features

*   **Empty Directory Detection**: Finds and lists all empty subdirectories.
*   **Aged Log File Identification**: Locates `.log` files older than a configurable threshold (default: 90 days).
*   **Temporary File Spotting**: Identifies common temporary file patterns (`.tmp`, `.bak`, files starting with `~`).

## Usage

```bash
python src/dust_bunny_collector.py <path_to_scan> [--max-log-age-days <days>]
```

**Example:**

```bash
python src/dust_bunny_collector.py ./my_project --max-log-age-days 180
```

This will scan `./my_project` and report dust bunnies, considering log files older than 180 days as aged.

## Output

The utility prints a categorized list of identified dust bunnies to standard output.

```
--- Cosmic Dust Bunny Report ---

Empty Directories:
  - /path/to/my_project/empty_folder

Aged Log Files (older than 90 days):
  - /path/to/my_project/logs/old.log (Last Modified: YYYY-MM-DD)

Temporary Files:
  - /path/to/my_project/temp/cache.tmp
  - /path/to/my_project/backup.bak

--- End Report ---
```

## Installation

This utility is self-contained and requires Python 3.6+.

1.  Navigate to the utility's directory:
    `cd utils/cosmic-dust-bunny-collector`
2.  Run directly:
    `python src/dust_bunny_collector.py .`

## Development

To run tests:

```bash
python -m unittest tests/test_dust_bunny_collector.py
```
