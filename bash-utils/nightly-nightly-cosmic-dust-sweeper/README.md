# Nightly Cosmic Dust Sweeper

## Overview

The `nightly-cosmic-dust-sweeper` is a whimsical yet practical Bash utility designed to help you maintain a tidy system by automatically identifying and removing old log files, temporary data, and other digital 'cosmic dust'. It's like a tiny, automated janitor for your file system, ensuring your directories remain pristine and performant.

## Features

*   **Age-based Pruning**: Delete files older than a specified number of days.
*   **Pattern Matching**: Target specific files using glob patterns (e.g., `*.log`, `temp_*`).
*   **Dry Run Mode**: See exactly what files *would* be deleted without actually removing them.
*   **Verbose Output**: Get detailed information about the sweeping process.
*   **Exclusion Paths**: Specify directories or files to explicitly ignore.

## Usage

```bash
./src/cosmic_dust_sweeper.sh -d <directory> -a <age_in_days> [-p <file_pattern>] [-x <exclude_path>] [--dry-run] [--verbose]
```

### Arguments:

*   `-d, --directory <path>`: **(Required)** The target directory to sweep for cosmic dust.
*   `-a, --age <days>`: **(Required)** Files older than this many days will be considered cosmic dust.
*   `-p, --pattern <glob>`: **(Optional)** A file pattern (e.g., `*.log`, `temp_*`) to match. If not provided, all files older than the specified age will be considered.
*   `-x, --exclude <path>`: **(Optional)** A path (file or directory) to exclude from the sweep. Can be specified multiple times.
*   `--dry-run`: **(Optional)** Simulate the sweep without actually deleting any files. Shows what *would* be removed.
*   `--verbose`: **(Optional)** Enable verbose output, showing each file considered and action taken.
*   `-h, --help`: **(Optional)** Display this help message.

### Examples:

1.  **Sweep all files older than 30 days in `/var/log` (dry run):**
    ```bash
    ./src/cosmic_dust_sweeper.sh -d /var/log -a 30 --dry-run
    ```

2.  **Delete `.tmp` files older than 7 days in `/tmp/my_app`:**
    ```bash
    ./src/cosmic_dust_sweeper.sh -d /tmp/my_app -a 7 -p "*.tmp"
    ```

3.  **Sweep `/home/user/data` for any file older than 90 days, excluding a specific subdirectory:**
    ```bash
    ./src/cosmic_dust_sweeper.sh -d /home/user/data -a 90 -x /home/user/data/important_archive
    ```

4.  **Verbose sweep of `/var/log` for `.gz` files older than 180 days:**
    ```bash
    ./src/cosmic_dust_sweeper.sh -d /var/log -a 180 -p "*.gz" --verbose
    ```

## Installation

Simply clone this repository or copy the `src/cosmic_dust_sweeper.sh` script to a convenient location on your system. Make it executable:

```bash
chmod +x src/cosmic_dust_sweeper.sh
```

## Automation (Cron Example)

To run the Cosmic Dust Sweeper automatically, you can add it to your system's cron schedule. For example, to run it daily at 2:00 AM to clean `/var/log` of files older than 60 days:

```cron
0 2 * * * /path/to/nightly-cosmic-dust-sweeper/src/cosmic_dust_sweeper.sh -d /var/log -a 60 > /dev/null 2>&1
```

Remember to replace `/path/to/nightly-cosmic-dust-sweeper/` with the actual path to the utility on your system.

## Contributing

Feel free to contribute to the Cosmic Dust Sweeper! Report issues, suggest features, or submit pull requests to help keep our digital cosmos clean.
