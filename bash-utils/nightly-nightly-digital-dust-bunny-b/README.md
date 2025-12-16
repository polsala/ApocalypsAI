# Nightly Digital Dust Bunny Buster

## Overview

The `nightly-digital-dust-bunny-buster` is a whimsical yet practical Bash utility designed to help you maintain a tidy filesystem. It scans a specified directory for files and subdirectories that haven't been modified for a certain number of days, identifying them as 'digital dust bunnies'. You can then choose to perform a dry run to see what would be removed, or initiate a full purge to clean them away.

This tool is perfect for regularly cleaning up temporary files, old downloads, forgotten logs, or any other digital clutter that accumulates over time, keeping your system lean and efficient.

## Features

*   **Age-based Identification**: Finds files and directories older than a configurable number of days.
*   **Targeted Scanning**: Specify any directory to scan, or use the current directory by default.
*   **Dry Run Mode**: Safely preview what would be deleted without making any changes.
*   **Interactive Purge**: Confirm deletions before they happen (unless forced).
*   **Force Delete Mode**: For automated cleanup, skip confirmation.
*   **Handles Special Characters**: Robustly deals with filenames containing spaces or special characters.

## Installation

This utility is a standalone Bash script. No special installation is required beyond ensuring you have Bash available on your system (which is standard on most Linux/macOS environments).

1.  Navigate to the `bash-utils/nightly-digital-dust-bunny-buster` directory.
2.  Make the script executable:
    ```bash
    chmod +x src/dust_bunny_buster.sh
    ```

## Usage

Run the script from its directory or add it to your PATH.

```bash
./src/dust_bunny_buster.sh [OPTIONS]
```

### Options

*   `-d <directory>`: Specify the target directory to scan (default: current directory `.`).
*   `-a <days>`: Specify the age in days for files/directories to be considered 'dust bunnies' (default: `7` days).
*   `-p`: Perform the purge (delete files/directories). By default, it's a dry run.
*   `-f`: Force deletion without confirmation (use with extreme caution, implies `-p`).
*   `-h`: Display the help message and exit.

### Examples

1.  **Dry run: Find files/directories in the current directory older than 7 days (default behavior):**
    ```bash
    ./src/dust_bunny_buster.sh
    ```

2.  **Dry run: Find files/directories in `/tmp` older than 30 days:**
    ```bash
    ./src/dust_bunny_buster.sh -d /tmp -a 30
    ```

3.  **Purge: Delete files/directories in `/var/log` older than 90 days (will prompt for confirmation):**
    ```bash
    ./src/dust_bunny_buster.sh -d /var/log -a 90 -p
    ```

4.  **Force Purge: Delete files/directories in `~/Downloads` older than 180 days (no confirmation):**
    ```bash
    ./src/dust_bunny_buster.sh -d ~/Downloads -a 180 -f
    ```

## How it Works

The script uses the `find` command to locate files and directories based on their modification time (`-mtime`). It then lists these identified 'dust bunnies'. If a purge is requested (`-p` or `-f`), it uses `xargs` and `rm -rf` to safely remove them. The `-mindepth 1 -maxdepth 1` options with `find` ensure that only items directly within the specified target directory are considered, preventing unintended deep dives into subdirectories unless they themselves are old enough to be removed as a whole.

## Contributing

Feel free to suggest improvements or report issues! Your contributions help keep the digital realm clean and tidy.
