# Nightly Digital Dust Bunny Sweeper

A whimsical Bash script to help you keep your digital environment tidy by finding and optionally sweeping away old, unused files – affectionately known as "digital dust bunnies." These forgotten files can accumulate in temporary directories, caches, and other nooks and crannies of your system, taking up space and potentially slowing things down.

This utility provides a safe "dry run" mode to identify these digital dust bunnies before you decide to sweep them away permanently.

## Features

*   **Identify Old Files**: Scans specified directories for files older than a configurable number of days.
*   **Dry Run Mode**: By default, it only lists the identified dust bunnies, allowing you to review them before deletion.
*   **Deletion Mode**: An optional flag to permanently remove the identified files. Use with caution!
*   **Multiple Directories**: Scan one or more directories in a single run.
*   **Verbose Output**: See more details about the scanning and sweeping process.

## Usage

```bash
./src/dust_bunny_sweeper.sh [OPTIONS] [DIRECTORY...]
```

### Options

*   `-a, --age DAYS`: Files older than `DAYS` will be considered dust bunnies (default: `7` days).
*   `-d, --delete`: **DANGER ZONE!** Delete the identified dust bunnies. Use with extreme caution, as this action is irreversible.
*   `-v, --verbose`: Show detailed output during operation, including which directories are being searched and which files are being swept.
*   `-h, --help`: Display the help message and exit.

### Arguments

*   `DIRECTORY...`: One or more directories to scan for dust bunnies. If no directories are specified, the script defaults to scanning `/tmp`.

## Examples

1.  **List all digital dust bunnies older than 30 days in `/var/log` (dry run):**
    ```bash
    ./src/dust_bunny_sweeper.sh -a 30 /var/log
    ```

2.  **Sweep away all dust bunnies older than 7 days from `/tmp` and `/var/cache`:**
    ```bash
    ./src/dust_bunny_sweeper.sh -d /tmp /var/cache
    ```

3.  **List dust bunnies older than the default 7 days in the default `/tmp` directory with verbose output:**
    ```bash
    ./src/dust_bunny_sweeper.sh -v
    ```

4.  **Display help message:**
    ```bash
    ./src/dust_bunny_sweeper.sh --help
    ```

## Installation

This is a standalone Bash script. No special installation is required beyond having Bash available on your system (which is standard on most Linux/macOS systems).

1.  Clone the `ApocalypsAI` repository.
2.  Navigate to the `bash-utils/nightly-digital-dust-bunny-sweeper` directory.
3.  Make the script executable:
    ```bash
    chmod +x src/dust_bunny_sweeper.sh
    ```

## Testing

To run the automated tests:

```bash
./tests/test_sweeper.sh
```

The tests create temporary directories and files to simulate various scenarios (old files, new files, multiple directories, deletion, etc.) and clean them up afterwards, ensuring a deterministic and isolated test environment.
