# Nightly Data Debris Duster

## Overview

In the post-apocalyptic digital landscape, even data can become... well, debris. The `Nightly Data Debris Duster` is a whimsical yet practical utility designed to help you identify and manage old, forgotten files that are cluttering your precious storage. Think of it as a digital scavenger, tidying up the remnants of past operations.

It scans specified directories for files older than a configurable threshold, then offers options to simply report them, move them to a 'quarantine' zone for later review, or permanently 'dust' them away.

## Features

*   **Debris Detection**: Scans directories for files older than a specified number of days.
*   **Whimsical Reporting**: Provides a clear, yet charmingly themed, report of detected data debris.
*   **Quarantine Protocol**: Safely moves detected files to a designated 'quarantine' directory, preserving them for a final decision.
*   **Dusting Protocol**: Permanently deletes detected files, freeing up space.
*   **Self-contained**: Written in Python 3.11, with no external dependencies beyond standard libraries.

## Usage

### Prerequisites

*   Python 3.11 or higher

### Running the Duster

Navigate to the `src` directory and run `duster.py` with the desired arguments.

```bash
python src/duster.py --help
```

```
usage: duster.py [-h] --path PATH [PATH ...] [--age DAYS] [--mode {report,quarantine,dust}] [--quarantine-dir DIR]

A whimsical utility to clear out old, unused files (data debris).

options:
  -h, --help            show this help message and exit
  --path PATH [PATH ...]
                        One or more directories to scan for data debris.
  --age DAYS            Files older than this many days will be considered debris (default: 90).
  --mode {report,quarantine,dust}
                        Operation mode: 'report' (default), 'quarantine', or 'dust'.
  --quarantine-dir DIR  Directory to move files to when in 'quarantine' mode. Required for 'quarantine' mode.
```

### Examples

1.  **Report data debris older than 180 days in `/tmp/my_data` and `/var/logs`:**
    ```bash
    python src/duster.py --path /tmp/my_data /var/logs --age 180 --mode report
    ```

2.  **Quarantine files older than 30 days from `/home/user/downloads` to `/tmp/quarantine_zone`:**
    ```bash
    python src/duster.py --path /home/user/downloads --age 30 --mode quarantine --quarantine-dir /tmp/quarantine_zone
    ```

3.  **Permanently dust away files older than 7 days from `/tmp/old_cache`:**
    ```bash
    python src/duster.py --path /tmp/old_cache --age 7 --mode dust
    ```

## Development

### Running Tests

Tests are located in the `tests/` directory. Navigate to the root of the `nightly-data-debris-duster` folder and run `pytest`.

```bash
python -m pytest tests/
```

## License

This utility is released under the MIT License. See the `LICENSE` file in the repository root for more details.
