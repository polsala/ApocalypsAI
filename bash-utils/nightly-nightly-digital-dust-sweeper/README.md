# Nightly Digital Dust Sweeper

A whimsical Bash utility to help you keep your digital wasteland tidy! It scans specified directories for "digital dust bunnies" – old, forgotten files, temporary artifacts, and empty directories – that might be cluttering your system. Think of it as a friendly scavenger bot, identifying prime candidates for cleanup without actually deleting anything (unless you choose to manually after review).

## Features

*   **Empty Directory Detection**: Finds directories that are completely empty.
*   **Aged File Identification**: Locates files older than a specified number of days.
*   **Temporary File Spotting**: Identifies common temporary and backup files (`.tmp`, `.bak`, `~`, `.log`, `.old`).
*   **Non-Destructive**: By default, it only lists the "dust bunnies," allowing you to review before taking action.

## Usage

```bash
./src/dust_sweeper.sh [OPTIONS]
```

### Options

*   `-p, --path <DIRECTORY>`: The directory to scan. Defaults to the current directory (`.`).
*   `-d, --days <NUMBER>`: Files older than this many days will be considered "old." Defaults to `30`.

### Examples

1.  **Scan the current directory for dust bunnies older than 30 days (default):**
    ```bash
    ./src/dust_sweeper.sh
    ```

2.  **Scan `/var/log` for files older than 60 days:**
    ```bash
    ./src/dust_sweeper.sh -p /var/log -d 60
    ```

3.  **Scan your home directory for any dust bunnies:**
    ```bash
    ./src/dust_sweeper.sh --path ~/
    ```

## How it Works

The script uses `find` commands to locate files and directories matching the criteria. It then prints them to standard output, categorized for easy review.

## Installation

This is a standalone Bash script. Simply download `src/dust_sweeper.sh` and make it executable:

```bash
chmod +x src/dust_sweeper.sh
```

## Running Tests

To ensure the Digital Dust Sweeper is working as expected, you can run its self-contained tests:

```bash
./tests/test_dust_sweeper.sh
```

The tests create a temporary directory with various files and directories, then run the `dust_sweeper.sh` script against it, verifying the output.
