# Digital Dust Bunny Sweeper

## Overview

In the grand scheme of preparing for the inevitable, a clean digital workspace is paramount. The `digital-dust-bunny-sweeper` is your trusty broom for sweeping away the digital detritus that accumulates over time. It identifies and helps you remove 'digital dust bunnies' – empty directories, old log files, and common temporary files – ensuring your filesystem remains lean, mean, and apocalypse-ready.

## Features

*   **Empty Directory Detection**: Finds and lists directories that contain no files or subdirectories.
*   **Old Log File Identification**: Locates log files (`.log`, `.txt` often used for logs) older than a specified number of days.
*   **Temporary File Cleanup**: Scans for common temporary file extensions (`.tmp`, `.bak`, `~`, `.swp`).
*   **Dry Run Mode (Default)**: Safely reports what *would* be deleted without making any changes.
*   **Deletion Mode**: With explicit `--delete` flag, it will proceed with the removal of identified files and directories.

## Usage

To scan a directory for dust bunnies (dry run):

```bash
python src/sweeper.py /path/to/scan
```

To scan and delete identified dust bunnies:

```bash
python src/sweeper.py /path/to/scan --delete
```

To specify a different age for 'old' log files (e.g., 60 days):

```bash
python src/sweeper.py /path/to/scan --log-age 60
```

## Installation

This utility is self-contained and requires no special installation beyond a standard Python 3.11+ environment.

## Example Output (Dry Run)

```
Scanning /home/user/project for digital dust bunnies...

--- Empty Directories Found ---
  - /home/user/project/empty_folder
  - /home/user/project/another_empty_dir

--- Old Log Files Found (older than 30 days) ---
  - /home/user/project/logs/app.log (last modified: 2023-01-01)
  - /home/user/project/data/old_report.txt (last modified: 2023-02-15)

--- Temporary Files Found ---
  - /home/user/project/temp.tmp
  - /home/user/project/config.bak

Dry run complete. No files or directories were deleted.
Run with --delete to remove these dust bunnies.
```
