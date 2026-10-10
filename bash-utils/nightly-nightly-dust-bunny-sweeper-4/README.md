# Nightly Dust Bunny Sweeper

## Summary

This utility, the "Nightly Dust Bunny Sweeper," is a whimsical-yet-useful Bash script designed to help you maintain a tidy digital environment. It identifies and offers to remove old, forgotten temporary files and empty directories that accumulate over time, much like physical dust bunnies under your server racks. By sweeping these digital remnants, you can reclaim disk space and keep your system clutter-free.

## Usage

To run the Dust Bunny Sweeper, execute the `dust_bunny_sweeper.sh` script with the target directory and the age (in days) of files/directories to consider for sweeping.

```bash
bash src/dust_bunny_sweeper.sh <target_directory> [age_in_days] [--dry-run] [--force]
```

### Arguments:

*   `<target_directory>`: The path to the directory where the sweeper will look for dust bunnies. **Caution: Be mindful of the directory you choose!**
*   `[age_in_days]`: Files and empty directories older than this many days will be considered for sweeping. If not provided, defaults to `30` days.
*   `--dry-run`: (Optional) Perform a dry run. The script will list what *would* be swept without actually deleting anything. This is highly recommended for a first run.
*   `--force`: (Optional) Skip the confirmation prompt and proceed with deletion immediately. Use with extreme caution.

### Examples:

*   **Dry run in /tmp for items older than 7 days:**
    ```bash
bash src/dust_bunny_sweeper.sh /tmp 7 --dry-run
    ```

*   **Sweep files in /var/log/old_logs older than 90 days (with confirmation):**
    ```bash
bash src/dust_bunny_sweeper.sh /var/log/old_logs 90
    ```

*   **Force sweep in ~/downloads for items older than 30 days (NO CONFIRMATION):**
    ```bash
bash src/dust_bunny_sweeper.sh ~/downloads 30 --force
    ```

## How it Works

The script uses the `find` command to locate files and empty directories within the specified `target_directory` that have not been modified for the given `age_in_days`. It then presents a list of these "dust bunnies" and, unless `--force` is used, prompts for confirmation before proceeding with their removal using `rm`.

## Safety First!

Always start with `--dry-run` to understand what the script will do. Be cautious when using `--force`, especially in critical system directories. This tool is designed for tidying up *temporary* or *known-to-be-disposable* areas.
