# Nightly Digital Dust Bunny Sweeper

In the post-apocalyptic digital wasteland, every byte of storage is precious. The `nightly-digital-dust-bunny` utility helps you reclaim valuable disk space by identifying "digital dust bunnies" – large, old, or duplicate files that might be lurking in your directories.

This whimsical-yet-useful Bash script provides a clear report, allowing you to review and decide which files to sweep away, ensuring your systems remain lean and efficient.

## Features

*   **Large File Detection**: Identifies files exceeding a configurable size threshold.
*   **Old File Detection**: Flags files that haven't been modified in a configurable number of days.
*   **Duplicate File Detection**: Finds identical files based on their MD5 hash, helping you eliminate redundant copies.
*   **Configurable Thresholds**: Easily adjust what constitutes a "large" or "old" file.
*   **Dry Run by Default**: Only generates a report; no files are deleted without explicit user action.

## Usage

To run the Digital Dust Bunny Sweeper, simply execute the script with an optional directory path. If no directory is provided, it will scan the current directory.

```bash
bash src/dust_bunny_sweeper.sh [OPTIONS] [DIRECTORY]
```

### Options

*   `-s <MB>`: Set the large file threshold in Megabytes. Files larger than this will be reported. (Default: 50MB)
*   `-o <DAYS>`: Set the old file threshold in days. Files older than this (based on last modification time) will be reported. (Default: 180 days)
*   `-h`: Display the help message and exit.

### Examples

Scan the current directory with default settings:
```bash
bash src/dust_bunny_sweeper.sh
```

Scan `/var/log` for files larger than 100MB or older than 365 days:
```bash
bash src/dust_bunny_sweeper.sh -s 100 -o 365 /var/log
```

Get help:
```bash
bash src/dust_bunny_sweeper.sh -h
```

## How it Works

The script uses standard Unix/Linux commands (`find`, `du`, `md5sum`, `sort`, `uniq`, `stat`, `awk`, `cut`, `bc`, `date`) to efficiently scan the specified directory. It categorizes findings into "Large Files", "Old Files", and "Duplicate Files" sections, providing details like size, last modification date, and file paths.

## Safety Note

This utility is designed for reporting only. It **does not delete any files**. Always review the generated report carefully before manually deleting any files. Consider making backups of critical data before performing any cleanup operations.
