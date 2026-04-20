# Nightly Digital Dust Bunny Sweeper

## Overview

Welcome, weary traveler of the digital plains! Are your directories cluttered with forgotten files and empty folders, gathering 'digital dust bunnies' and 'cyber cobwebs'? The `nightly-digital-dust-bunny-sweeper` is here to help!

This whimsical Bash script scans specified directories for files older than a certain age and for empty directories. It then provides a charming report of its findings and, if you dare, can perform a 'sweep' to clean them up.

## Features

*   **Find Old Files**: Identifies files that haven't been touched in a configurable number of days.
*   **Locate Empty Directories**: Pinpoints directories that serve no purpose, like abandoned digital nests.
*   **Dry Run Mode**: Safely preview what would be cleaned without making any changes.
*   **Interactive Sweep**: Confirm deletions before they happen, or run fully automated.
*   **Whimsical Reporting**: Get a delightful summary of your digital decluttering efforts.

## Usage

```bash
./src/dust_bunny_sweeper.sh [OPTIONS]
```

### Options

*   `-d, --dir <path>`: The target directory to scan. Defaults to the current directory (`.`).
*   `-a, --age <days>`: Files older than this many days will be considered 'dust bunnies'. Defaults to `30` days.
*   `-e, --empty-only`: Only find and report empty directories (no old files).
*   `-f, --files-only`: Only find and report old files (no empty directories).
*   `-s, --sweep`: Perform the actual cleanup (delete files/directories). **Use with caution!**
*   `-y, --yes`: Automatically confirm all deletions when using `--sweep` (non-interactive).
*   `-h, --help`: Display this help message.

### Examples

1.  **Find dust bunnies and cobwebs in the current directory (dry run, default age 30 days):**
    ```bash
    ./src/dust_bunny_sweeper.sh
    ```

2.  **Find dust bunnies older than 7 days in `/var/log` (dry run):**
    ```bash
    ./src/dust_bunny_sweeper.sh --dir /var/log --age 7
    ```

3.  **Find only empty directories in your home folder (dry run):**
    ```bash
    ./src/dust_bunny_sweeper.sh --dir ~/ --empty-only
    ```

4.  **Perform a full sweep of old files (older than 90 days) in `/tmp`, asking for confirmation:**
    ```bash
    ./src/dust_bunny_sweeper.sh --dir /tmp --age 90 --sweep
    ```

5.  **Automate a sweep of old files and empty directories in `/old_backups` without confirmation:**
    ```bash
    ./src/dust_bunny_sweeper.sh --dir /old_backups --age 180 --sweep --yes
    ```

## Installation

Simply copy the `src/dust_bunny_sweeper.sh` script to a location in your `PATH` or execute it directly.

```bash
chmod +x src/dust_bunny_sweeper.sh
```

## Contributing

If you have ideas for more whimsical features or bug fixes, feel free to contribute! Let's keep our digital realms tidy and delightful.
