# Nightly Temporal Dust Bunny Sweeper

## Overview
In the digital realm, just like in our physical spaces, forgotten detritus accumulates. These are the 'temporal dust bunnies' – old temporary files and directories that linger, consuming precious disk space and occasionally causing digital clutter. The `nightly-temp-dust-bunny-sweeper` is a whimsical yet practical Bash utility designed to automatically seek out and sweep away these digital remnants.

It's perfect for maintaining a tidy system, especially in environments where temporary files can quickly pile up, ensuring your digital abode remains spick and span.

## Features
*   **Age-based Deletion**: Targets files and directories older than a specified number of days.
*   **Configurable Target**: Allows specifying any directory to sweep, not just the default `/tmp`.
*   **Dry Run Mode**: Preview what would be deleted without actually performing the sweep, for peace of mind.
*   **Verbose Output**: See exactly which temporal dust bunnies are being swept away.
*   **Safety Checks**: Includes basic validation for target directories and age parameters.

## Usage

```bash
./src/main.sh [-d <directory>] [-a <days>] [-n] [-v] [-h]
```

### Arguments
*   `-d <directory>`: **Target directory to sweep.** (Default: `/tmp`)
    *   *Caution*: Be mindful when specifying critical system directories. The script includes a warning for common critical paths but will proceed if explicitly told.
*   `-a <days>`: **Age in days** for files/directories to be considered 'dust bunnies'. Items modified *more than* this many days ago will be targeted. (Default: `7`)
*   `-n`: **Dry run mode.** Shows what would be deleted without actually deleting anything.
*   `-v`: **Verbose output.** Lists each file/directory as it is processed (or would be processed in dry run).
*   `-h`: Display this help message and exit.

### Examples

1.  **Sweep `/tmp` for items older than 7 days (default behavior):**
    ```bash
    ./src/main.sh
    ```

2.  **Sweep `/var/log/old_temp` for items older than 30 days:**
    ```bash
    ./src/main.sh -d /var/log/old_temp -a 30
    ```

3.  **Perform a dry run on `/home/user/downloads` for items older than 14 days, with verbose output:**
    ```bash
    ./src/main.sh -d /home/user/downloads -a 14 -n -v
    ```

4.  **Sweep `/tmp` with verbose output:**
    ```bash
    ./src/main.sh -v
    ```

## How it Works
The script uses the `find` command to locate files and directories within the specified `TARGET_DIR` that have a modification time (`-mtime`) older than `AGE_DAYS`. It then uses `rm -rf` to remove these identified 'temporal dust bunnies'. The `-mindepth 1 -maxdepth 1` options ensure that only direct children of the target directory are considered for deletion, preventing accidental sweeps of the target directory itself or unintended deep dives into sub-subdirectories that might not be old enough at their root level.
