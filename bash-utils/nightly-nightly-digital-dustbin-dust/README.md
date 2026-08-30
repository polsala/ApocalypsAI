# Nightly Digital Dustbin Duster

A whimsical Bash script designed to help you tidy up your digital workspace by identifying and offering to clean up old, forgotten files. Before deletion, each file receives a poetic send-off, ensuring its bits find peace in the great beyond (or at least, off your disk).

## Features

*   **Whimsical Eulogies**: Each file slated for deletion gets a unique, lighthearted farewell message.
*   **Configurable Scan**: Specify the directory to scan and the age threshold for "old" files.
*   **Dry Run Mode**: Preview which files would be deleted without actually removing them.
*   **Interactive Confirmation**: Prompts for user confirmation before proceeding with actual deletion.

## Usage

```bash
./src/dustbin_duster.sh [DIRECTORY] [DAYS_OLD] [--dry-run]
```

### Arguments

*   `DIRECTORY` (optional): The path to the directory you want to scan. Defaults to `/tmp` if not provided.
*   `DAYS_OLD` (optional): Files older than this many days will be considered for deletion. Defaults to `7` days if not provided.
*   `--dry-run` (optional): If specified, the script will list files and their eulogies but will not perform any deletions. This is useful for previewing the cleanup.

### Examples

Scan `/var/log` for files older than 30 days and perform a dry run:
```bash
./src/dustbin_duster.sh /var/log 30 --dry-run
```

Clean up files in `/tmp` older than 1 day (will prompt for confirmation):
```bash
./src/dustbin_duster.sh /tmp 1
```

Use default settings (scan `/tmp` for files older than 7 days):
```bash
./src/dustbin_duster.sh
```

## Installation

This is a standalone Bash script. Simply download `src/dustbin_duster.sh` and make it executable:

```bash
chmod +x src/dustbin_duster.sh
```

## Testing

The utility includes a self-contained test script. To run the tests:

```bash
./tests/test_dustbin_duster.sh
```

The tests use mocks for `find`, `rm`, `read`, and `shuf` to ensure deterministic and safe execution without altering your actual file system or requiring interactive input.
