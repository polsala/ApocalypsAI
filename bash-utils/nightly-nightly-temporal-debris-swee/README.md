# Nightly Temporal Debris Sweeper

## Overview

The `nightly-temporal-debris-sweeper` is a whimsical Bash utility designed to help you maintain a pristine digital environment by purging old, forgotten temporary files. It scans specified directories for "temporal debris" (files older than a certain age) and, with your command, initiates a "purge sequence" to remove them, all while reporting its actions with dramatic, post-apocalyptic flair.

Think of it as your digital janitor, but with a flair for the dramatic and a mission to keep your system free from the detritus of forgotten timelines.

## Features

*   **Configurable Target Directory**: Specify which directory to scan for debris.
*   **Configurable Age Threshold**: Define how old a file must be to be considered "temporal debris".
*   **Dry Run Mode**: Preview which files would be deleted without actually performing the purge.
*   **Force Delete**: Skip confirmation prompts for automated purges.
*   **Whimsical Output**: Enjoy dramatic messages as your system is cleansed.

## Usage

```bash
./src/sweep_debris.sh [-d <directory>] [-a <days>] [--dry-run] [--force] [--help]
```

### Arguments:

*   `-d <directory>` or `--directory <directory>`: The target directory to sweep for debris. Defaults to `/tmp`.
*   `-a <days>` or `--age <days>`: The age in days for files to be considered debris. Files older than this will be targeted. Defaults to `7` days.
*   `--dry-run`: Lists the files that *would* be deleted, but performs no actual deletion. Useful for previewing the purge.
*   `--force`: Deletes files without asking for confirmation. Use with caution!
*   `--help`: Displays the usage information and exits.

### Examples:

1.  **Scan `/var/log` for files older than 30 days (dry run):**
    ```bash
    ./src/sweep_debris.sh -d /var/log -a 30 --dry-run
    ```

2.  **Purge `/tmp` of files older than 7 days, with confirmation:**
    ```bash
    ./src/sweep_debris.sh
    # (Will prompt for confirmation before deleting)
    ```

3.  **Force purge `/home/user/cache` of files older than 1 day:**
    ```bash
    ./src/sweep_debris.sh -d /home/user/cache -a 1 --force
    ```

## Installation

This is a standalone Bash script. Simply ensure it's executable:

```bash
chmod +x src/sweep_debris.sh
```

## Testing

To run the automated tests for this utility, navigate to the utility's root directory and execute the test script:

```bash
chmod +x tests/test_sweep_debris.sh
./tests/test_sweep_debris.sh
```

The tests will create temporary directories and files to simulate various scenarios (no debris, dry run, forced purge, interactive purge, etc.) and verify the script's behavior and output.
