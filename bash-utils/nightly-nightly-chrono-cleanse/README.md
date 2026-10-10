# Nightly Chrono-Cleanse

A whimsical Bash utility designed to help you maintain a tidy digital environment by purging old, forgotten files from specified directories. Think of it as a temporal janitor, sweeping away the digital dust that accumulates over time.

## Features

*   **Targeted Cleaning**: Specify one or more directories to cleanse.
*   **Age-Based Purge**: Define how old a file must be (in days) before it's considered 'ancient digital dust'.
*   **Dry Run Mode**: Preview what files *would* be deleted without actually removing them, for peace of mind.
*   **Whimsical Output**: Enjoy a touch of charm with every cleanse.

## Usage

```bash
./src/chrono_cleanse.sh [OPTIONS] -d <directory1> [-d <directory2> ...] 
```

### Options:

*   `-d <directory>`: Specify a directory to cleanse. This option can be used multiple times to target multiple directories.
*   `-a <age_in_days>`: Files older than this many days will be targeted for deletion. Defaults to `30` days.
*   `-n` or `--dry-run`: Perform a dry run. The script will report which files *would* be deleted, but won't actually remove them.
*   `-h` or `--help`: Display this help message.

## Examples

1.  **Clean files older than 60 days in `/var/log` and `/tmp` (dry run):**

    ```bash
    ./src/chrono_cleanse.sh -n -a 60 -d /var/log -d /tmp
    ```

2.  **Actually delete files older than 7 days in `~/downloads`:**

    ```bash
    ./src/chrono_cleanse.sh -a 7 -d ~/downloads
    ```

3.  **Clean files older than the default 30 days in a single directory:**

    ```bash
    ./src/chrono_cleanse.sh -d /path/to/old/data
    ```

## Installation

This is a standalone Bash script. Simply clone the repository and ensure the script is executable:

```bash
chmod +x src/chrono_cleanse.sh
```

## Safety First!

Always use the `--dry-run` option first to understand what will be deleted. Be cautious when running deletion scripts, especially with elevated privileges. The `find` command used targets *files* only (`-type f`) to prevent accidental directory removal, but always double-check your target directories and age thresholds.
