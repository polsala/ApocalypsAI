# Nightly Chrono-Clutter Cleaner

The digital world accumulates "chrono-clutter" – temporary files, old backups, and forgotten logs that linger like digital dust bunnies, slowing down your systems and consuming precious storage. The Nightly Chrono-Clutter Cleaner is here to help!

This whimsical-yet-useful bash utility helps you identify and optionally sweep away these temporal anomalies from your directories, ensuring your digital spaces remain pristine and efficient.

## Features

*   **Targeted Cleaning**: Specify a directory to scan for clutter.
*   **Age-Based Detection**: Only targets files older than a configurable number of days.
*   **Pattern Matching**: Uses flexible file patterns (e.g., `*.tmp`, `*.bak`, `~*`) to identify specific types of clutter.
*   **Dry Run Mode**: Safely preview which files would be deleted before committing to cleanup.
*   **Cleanup Mode**: Confidently remove identified clutter.

## Usage

```bash
./src/chrono-clutter-cleaner.sh [OPTIONS]
```

### Options

*   `-d <directory>`: **Target directory** to scan for clutter. Defaults to the current directory (`.`).
*   `-a <days>`: **Age threshold** in days. Files older than this many days will be considered clutter. Defaults to `30`.
*   `-p <pattern1,pattern2,...>`: **Comma-separated list of file patterns** to match. Wildcards (`*`, `?`) are supported. Defaults to `'*.tmp,*.bak,~*,#*#'`.
*   `-c`: **Cleanup mode**. If this flag is present, the identified files will be *deleted*. By default, the script runs in **dry-run mode** and only lists files.
*   `-h`: Display this help message and exit.

## Examples

1.  **Dry run in the current directory for files older than 7 days with default patterns:**
    ```bash
    ./src/chrono-clutter-cleaner.sh -a 7
    ```

2.  **Cleanup old log files (`*.log`) in `/var/log/archive` that are older than 90 days:**
    ```bash
    ./src/chrono-clutter-cleaner.sh -d /var/log/archive -a 90 -p "*.log" -c
    ```

3.  **Find all temporary files (`*.tmp`) and old configuration backups (`*.conf.bak`) in your home directory, but only list them (dry run):**
    ```bash
    ./src/chrono-clutter-cleaner.sh -d ~/ -p "*.tmp,*.conf.bak"
    ```

4.  **Perform a full cleanup of default clutter patterns in `/tmp` for files older than 1 day:**
    ```bash
    ./src/chrono-clutter-cleaner.sh -d /tmp -a 1 -c
    ```

## Installation

This is a standalone bash script. Simply ensure it's executable:

```bash
chmod +x src/chrono-clutter-cleaner.sh
```

Then run it as shown in the usage examples.

## Testing

To run the automated tests, navigate to the utility's root directory and execute:

```bash
./tests/test_chrono-clutter-cleaner.sh
```

The tests create temporary directories and files to simulate various scenarios, ensuring the cleaner correctly identifies and removes (or lists) files based on age and patterns without affecting your actual filesystem.
