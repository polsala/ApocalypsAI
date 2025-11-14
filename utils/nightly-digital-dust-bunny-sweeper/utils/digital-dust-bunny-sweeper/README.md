# Digital Dust Bunny Sweeper

## Overview

In the vast digital landscapes of our repositories, tiny specks of forgotten data accumulate, forming 'digital dust bunnies'. These are often empty directories, ancient log files, or temporary artifacts left behind by long-finished processes. While harmless, they can clutter your workspace and obscure the true state of your project.

The Digital Dust Bunny Sweeper is a whimsical-yet-useful utility designed to help you identify these digital dust bunnies. It scans a specified directory, reporting on:

*   **Empty Directories**: Folders that contain no files or subdirectories.
*   **Aged Temporary/Log Files**: Files matching common temporary or log patterns (`.log`, `.tmp`, `temp_`, etc.) that haven't been modified in a specified number of days.

**Important**: This utility is a *reporter* only. It will never delete or modify any files. Its purpose is to provide you with an actionable list, allowing you to decide what to sweep away.

## Usage

To run the sweeper, navigate to the `digital-dust-bunny-sweeper` directory and execute the `sweeper.py` script.

```bash
python src/sweeper.py --path /path/to/scan [--age-days 30] [--patterns "*.log" "*.tmp"]
```

### Arguments:

*   `--path <directory>`: The root directory from which to start scanning for dust bunnies. (Required)
*   `--age-days <int>`: The minimum age in days for files to be considered 'old'. Defaults to 30 days. (Optional)
*   `--patterns <pattern1> <pattern2> ...`: A space-separated list of glob patterns (e.g., `*.log`, `*.tmp`, `temp_*`) for files to check by age. Defaults to `['*.log', '*.tmp', 'temp_*']`. (Optional)

## Example Output

```
Scanning /my/project for digital dust bunnies...

--- Empty Directories ---
- /my/project/build/empty_cache
- /my/project/docs/old_drafts/unused

--- Aged Files (older than 30 days) ---
- /my/project/logs/debug.log (Last modified: 2023-01-15)
- /my/project/temp/upload_20230201.tmp (Last modified: 2023-02-01)

Sweeping complete! No digital dust bunnies found. Your digital space is sparkling clean!
```

## Development

This utility is written in Python 3.11 and uses only standard library modules (`os`, `time`, `argparse`, `fnmatch`, `datetime`).

## Tests

Tests are located in `tests/test_sweeper.py` and can be run using `unittest`:

```bash
python -m unittest tests/test_sweeper.py
```
