# Nightly Resource Scavenger

The Nightly Resource Scavenger is a whimsical-yet-useful utility designed to help maintain system hygiene by identifying and optionally cleaning up old, temporary, or otherwise forgotten files that accumulate over time. Think of it as a digital janitor, tidying up the digital rubble before it becomes an apocalyptic mess.

## Features

*   **Age-based Cleanup**: Find files older than a specified number of days.
*   **Pattern Matching**: Filter files by specific substrings in their names (e.g., `.tmp`, `cache_`, `~`).
*   **Dry Run Mode**: Safely preview which files would be deleted without actually removing them.
*   **Recursive Scan**: Scans subdirectories to ensure no digital dust bunny is missed.

## Usage

The scavenger is a Python 3.11 script that can be run from the command line.

```bash
python src/scavenger.py <directory> [--days-old <int>] [--patterns <pattern1> <pattern2> ...] [--delete]
```

### Arguments

*   `<directory>` (required): The root directory to start scanning from.
*   `--days-old <int>`: Files older than this many days will be considered for cleanup. Defaults to `30`.
*   `--patterns <pattern1> <pattern2> ...`: Optional. A space-separated list of substrings to match in filenames. Only files containing at least one of these patterns will be considered. If not provided, all old files are considered.
*   `--delete`: **WARNING**: Use this flag to perform actual deletion. By default, the script runs in a dry-run mode, only listing files that *would* be deleted.

### Examples

1.  **Dry run: List all files in `/var/log` older than 60 days:**
    ```bash
    python src/scavenger.py /var/log --days-old 60
    ```

2.  **Dry run: List `.tmp` and `cache_` files in `/tmp` older than 7 days:**
    ```bash
    python src/scavenger.py /tmp --days-old 7 --patterns .tmp cache_
    ```

3.  **Perform actual deletion: Remove `.bak` files in `/home/user/data` older than 90 days:**
    ```bash
    python src/scavenger.py /home/user/data --days-old 90 --patterns .bak --delete
    ```

## Development & Testing

The utility is written in Python 3.11 and uses standard library modules.

### Running Tests

To run the automated tests, navigate to the utility's root directory (`utils/nightly-resource-scavenger/`) and execute:

```bash
python -m unittest tests/test_scavenger.py
```

Tests are deterministic and use `unittest.mock` to simulate filesystem operations and `datetime` for consistent time-based checks, ensuring they run offline without affecting your actual system.
