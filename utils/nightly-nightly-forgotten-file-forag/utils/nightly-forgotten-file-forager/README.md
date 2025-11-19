# Nightly Forgotten File Forager

## Overview

The `nightly-forgotten-file-forager` is a command-line utility designed to help you reclaim disk space by identifying and optionally removing files that haven't been modified in a long time. Think of it as a digital scavenger, tidying up the digital rubble of your system.

It's particularly useful for cleaning up old logs, temporary build artifacts, forgotten downloads, or any other digital detritus that accumulates over time.

## Usage

```bash
python src/forager.py --help
```

```
usage: forager.py [-h] --path PATH [--days DAYS] [--dry-run] [--confirm]

A whimsical utility to forage for and remove old, forgotten files.

options:
  -h, --help            show this help message and exit
  --path PATH           The root directory to start foraging from.
  --days DAYS           Files older than this many days will be considered 'forgotten'. Defaults to 30 days.
  --dry-run             Simulate the deletion process without actually removing any files.
  --confirm             Proceed with deletion without asking for confirmation (use with caution!).
```

### Examples

1.  **Find files older than 60 days in your downloads folder (dry run):**
    ```bash
    python src/forager.py --path ~/Downloads --days 60 --dry-run
    ```

2.  **Delete files older than 90 days in a project's `build/` directory (with confirmation):**
    ```bash
    python src/forager.py --path ./my_project/build --days 90
    ```

3.  **Automatically delete files older than 7 days in a temporary directory (no confirmation):**
    ```bash
    python src/forager.py --path /tmp/old_logs --days 7 --confirm
    ```

## Development

This utility is written in Python 3.11 and is self-contained. No external dependencies are required beyond the standard library.

## Tests

To run the tests, navigate to the `utils/nightly-forgotten-file-forager/` directory and execute:

```bash
python -m unittest tests/test_forager.py
```
