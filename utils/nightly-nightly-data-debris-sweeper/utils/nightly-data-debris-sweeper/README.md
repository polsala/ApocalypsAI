# Nightly Data Debris Sweeper

## Overview

The Nightly Data Debris Sweeper is a whimsical-yet-useful utility designed to help you maintain a clean and organized digital environment. In the post-apocalyptic landscape of your file system, temporary files, old logs, and empty directories can accumulate like digital rubble. This tool helps you sweep away this 'debris' based on age and file patterns, ensuring your valuable storage isn't wasted.

It operates in two modes: a `dry-run` to show you what *would* be removed, and an `execute` mode to perform the actual cleanup.

## Usage

```bash
python src/sweeper.py --path /path/to/clean --age 7 --patterns '*.log' '*.tmp' '__pycache__' --dry-run
```

### Arguments:

*   `--path <directory>`: The root directory to start sweeping from. (Required)
*   `--age <days>`: Files and empty directories older than this many days will be considered for removal. (Required, integer)
*   `--patterns <pattern1> <pattern2> ...`: One or more file patterns (e.g., `*.log`, `*.tmp`, `__pycache__`). Only files matching these patterns will be considered. If no patterns are provided, all files older than `--age` will be considered. (Optional)
*   `--dry-run`: If present, the utility will only report what *would* be deleted, without making any changes. (Optional)

## Examples

1.  **Dry-run to see old log files in your project directory (older than 30 days):**
    ```bash
    python src/sweeper.py --path ./my_project --age 30 --patterns '*.log' --dry-run
    ```

2.  **Clean up all temporary files and Python cache directories older than 7 days in your downloads folder:**
    ```bash
    python src/sweeper.py --path ~/Downloads --age 7 --patterns '*.tmp' '__pycache__' --execute
    ```

3.  **Remove any file older than 1 day in a specific temporary folder (use with caution!):**
    ```bash
    python src/sweeper.py --path /var/tmp/my_app_temp --age 1 --execute
    ```

## Installation

This utility is self-contained and requires Python 3.11+. No external dependencies are strictly needed beyond standard library modules.

To run:

```bash
cd utils/nightly-data-debris-sweeper
python src/sweeper.py --help
```
