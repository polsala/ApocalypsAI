# Cosmic Dust Bunny Collector

## Overview

The `cosmic-dust-bunny-collector` is your trusty broom for sweeping away the digital detritus that accumulates in your filesystem. It helps you identify and optionally remove two common types of 'dust bunnies':

1.  **Empty Directories**: Folders that serve no purpose other than taking up space and making your directory structure look messy.
2.  **Old Files**: Files that haven't been accessed or modified in a long, long time, suggesting they might be forgotten or obsolete.

Keep your digital space tidy and efficient, just like a well-maintained spaceship!

## Usage

Run the collector from your terminal. It requires a target path and can optionally take an age threshold for old files and a dry-run flag.

```bash
python3 src/collector.py --path /path/to/scan [--days-old <N>] [--dry-run]
```

### Arguments:

*   `--path <directory>` (required): The root directory from which to start scanning for dust bunnies.
*   `--days-old <N>` (optional): If provided, the utility will also look for files older than `N` days (based on last modification time). Set to `0` to disable this scan. Default is `0`.
*   `--dry-run` (optional): If set, the utility will only list the dust bunnies it *would* remove, without actually deleting anything. This is highly recommended for a first run!

## Examples

1.  **Find only empty directories in your home folder (dry-run):**
    ```bash
    python3 src/collector.py --path ~/ --dry-run
    ```

2.  **Find and delete empty directories and files older than 90 days in a project folder:**
    ```bash
    python3 src/collector.py --path /path/to/my/project --days-old 90
    ```

3.  **List all files older than 365 days in a backup directory (dry-run):**
    ```bash
    python3 src/collector.py --path /mnt/backups --days-old 365 --dry-run
    ```
