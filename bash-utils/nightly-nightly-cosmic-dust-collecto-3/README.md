# Nightly Cosmic Dust Collector

The digital cosmos can get messy! Over time, log files, temporary data, and other forgotten digital detritus accumulate, much like cosmic dust, cluttering your precious disk space. The Nightly Cosmic Dust Collector is here to help! This whimsical yet powerful Bash utility meticulously sweeps away files older than a specified age, keeping your systems tidy and optimized.

## Features

*   **Age-based Deletion**: Removes files older than a specified number of days.
*   **Dry Run Mode**: Preview which files would be deleted without actually removing them.
*   **Verbose Output**: See detailed information about the cleaning process.
*   **Safe**: Uses `find` and `rm` with care.

## Usage

```bash
./src/cosmic_dust_collector.sh <directory_path> <age_in_days> [--dry-run] [--verbose]
```

### Arguments

*   `<directory_path>`: The path to the directory where cosmic dust (old files) needs to be collected.
*   `<age_in_days>`: Files older than this many days will be targeted for deletion.
*   `--dry-run`: (Optional) Simulate the deletion process. Files will be listed but not actually removed.
*   `--verbose`: (Optional) Provide more detailed output about the script's actions.

## Examples

1.  **Preview files older than 30 days in `/var/log`:**
    ```bash
    ./src/cosmic_dust_collector.sh /var/log 30 --dry-run --verbose
    ```

2.  **Actually delete files older than 7 days in `/tmp/old_data`:**
    ```bash
    ./src/cosmic_dust_collector.sh /tmp/old_data 7 --verbose
    ```

3.  **Delete files older than 1 day in the current directory (quietly):**
    ```bash
    ./src/cosmic_dust_collector.sh . 1
    ```

## Installation

Simply place the `cosmic_dust_collector.sh` script in your desired location, ensure it's executable (`chmod +x src/cosmic_dust_collector.sh`), and run it.

## Automated Cleanup (e.g., with Cron)

To schedule regular cosmic dust collection, you can add an entry to your crontab:

```cron
# Run every night at 2 AM to clean /var/log, removing files older than 60 days
0 2 * * * /path/to/nightly-cosmic-dust-collector/src/cosmic_dust_collector.sh /var/log 60 >> /var/log/cosmic_dust_collector.log 2>&1
```

Remember to adjust the path and parameters to fit your system's needs.
