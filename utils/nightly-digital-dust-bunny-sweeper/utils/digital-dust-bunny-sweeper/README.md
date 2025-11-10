# Digital Dust Bunny Sweeper

## Purpose
Don't let your digital space get cluttered with forgotten bits and bytes! The Digital Dust Bunny Sweeper is a whimsical-yet-useful utility designed to help you declutter your filesystem. It identifies and optionally cleans up 'digital dust bunnies' – specifically, empty directories and old log files that might be hogging space or just making things messy.

## Features
- **Empty Directory Detection**: Finds directories that contain no files or subdirectories.
- **Old Log File Cleanup**: Identifies log files (`.log`, `.txt` by default) older than a specified number of days.
- **Dry Run Mode**: Preview what would be deleted without making any changes.
- **Configurable**: Easily adjust log file extensions and age thresholds.

## Usage

To run the sweeper, navigate to the `digital-dust-bunny-sweeper` directory and execute the `sweeper.py` script with your desired options.

```bash
python src/sweeper.py <path_to_scan> [OPTIONS]
```

### Arguments
- `<path_to_scan>`: The root directory from which to start scanning for dust bunnies.

### Options
- `--dry-run`: (Optional) Perform a dry run. The utility will report what *would* be deleted without actually deleting anything. Highly recommended for a first run!
- `--delete-empty-dirs`: (Optional) Enable deletion of empty directories found during the scan.
- `--delete-old-logs <days>`: (Optional) Enable deletion of log files older than the specified number of `days`. Default log extensions are `.log` and `.txt`.
- `--log-extensions <ext1> <ext2> ...`: (Optional) Specify custom log file extensions to consider (e.g., `--log-extensions .log .out .tmp`). Overrides default.

### Examples

1. **Dry run to see empty directories in your home folder:**
   ```bash
   python src/sweeper.py ~/ --dry-run --delete-empty-dirs
   ```

2. **Dry run to see log files older than 30 days in a project folder:**
   ```bash
   python src/sweeper.py /path/to/my/project --dry-run --delete-old-logs 30
   ```

3. **Actually delete empty directories and `.tmp` files older than 7 days in a specific directory:**
   ```bash
   python src/sweeper.py /var/log/app --delete-empty-dirs --delete-old-logs 7 --log-extensions .tmp
   ```

## Installation
This utility is self-contained and requires no special installation beyond a Python 3.x interpreter. Just clone the repository and run it!
