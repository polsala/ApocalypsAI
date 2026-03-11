# Nightly Digital Dust Bunny Sweeper

## Overview

The `nightly-digital-dust-bunny-sweeper` is a whimsical yet practical utility designed to help you maintain a tidy digital environment. It identifies and, optionally, removes "digital dust bunnies" – temporary files, old logs, and cache files – that accumulate over time in specified directories. By sweeping these away, you can reclaim valuable disk space and keep your system running smoothly.

## Features

*   **Configurable Directories**: Specify which directories to scan for old files.
*   **Age-Based Deletion**: Only target files older than a configurable number of days.
*   **Dry Run Mode**: Safely preview which files *would* be deleted without making any changes.
*   **Real Run Mode**: Execute deletions after you're confident in the dry run results.
*   **Verbose Output**: Get detailed information about each file being processed or deleted.
*   **Space Savings Report**: Provides a summary of the total files and disk space freed.

## Usage

To run the Digital Dust Bunny Sweeper, execute the `dust_bunny_sweeper.sh` script. It supports command-line arguments and environment variables for configuration.

```bash
./src/dust_bunny_sweeper.sh [OPTIONS]
```

### Options

*   `-d <dir>`: Add a directory to scan. Can be used multiple times. If used, it overrides the default directories. (e.g., `-d /var/log -d /tmp`)
*   `-a <days>`: Set the maximum age in days for files to be considered dust bunnies. Files older than this will be targeted. (e.g., `-a 30` for files older than 30 days)
*   `-r`: Enable "real run" mode. This will actually delete files. **Use with caution!** By default, the script runs in dry-run mode.
*   `-v`: Enable verbose output, showing each file that is processed or deleted.
*   `-h`: Display the help message and exit.

### Environment Variables

You can also configure the script using environment variables, which are useful for automated runs.

*   `DUST_BUNNY_DIRS`: A space-separated list of directories to scan. (e.g., `DUST_BUNNY_DIRS="/tmp /var/log"`)
*   `DUST_BUNNY_MAX_AGE`: The maximum age in days for files. (e.g., `DUST_BUNNY_MAX_AGE=14`)
*   `DUST_BUNNY_REAL_RUN`: Set to `true` to enable real deletions. (e.g., `DUST_BUNNY_REAL_RUN=true`)

Command-line arguments take precedence over environment variables.

## Examples

### 1. Dry Run (default behavior)

Scan default directories (`/tmp`, `/var/log`, `$HOME/.cache`) for files older than 7 days, showing what *would* be deleted:

```bash
./src/dust_bunny_sweeper.sh
```

### 2. Real Run with Custom Directory and Age

Delete files older than 30 days in `/var/cache/apt` and `/var/tmp`:

```bash
./src/dust_bunny_sweeper.sh -d /var/cache/apt -d /var/tmp -a 30 -r
```

### 3. Verbose Dry Run

See detailed output of files that would be deleted in `/tmp` older than 1 day:

```bash
./src/dust_bunny_sweeper.sh -d /tmp -a 1 -v
```

### 4. Using Environment Variables for a Scheduled Task

```bash
export DUST_BUNNY_DIRS="/opt/app/logs /home/user/.local/share/Trash"
export DUST_BUNNY_MAX_AGE=60
export DUST_BUNNY_REAL_RUN=true
./src/dust_bunny_sweeper.sh
```

## Dependencies

*   `bash` (version 4.0+ recommended)
*   `find`
*   `rm`
*   `du`
*   `awk`
*   `numfmt` (from GNU coreutils, for human-readable size output. If not available, size output will be in bytes.)

## Contributing

Feel free to contribute to the Digital Dust Bunny Sweeper! Suggestions for new features, bug reports, or pull requests are welcome.
