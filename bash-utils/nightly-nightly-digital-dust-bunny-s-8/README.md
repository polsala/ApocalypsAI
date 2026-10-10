# Nightly Digital Dust Bunny Sweeper

## Summary
This utility acts as a diligent digital janitor, scanning your specified directories for 'temporal detritus' – that is, files older than a certain age and empty directories. It helps you identify and optionally sweep away these 'digital dust bunnies' to keep your system tidy and efficient.

## Usage

Run the `dust_bunny_sweeper.sh` script with optional arguments to specify the target directory, the age threshold for files, and the action to perform.

```bash
./src/dust_bunny_sweeper.sh [-d <directory>] [-a <age_in_days>] [-c <action>]
```

### Arguments:
*   `-d <directory>`: The target directory to scan. Defaults to the current directory (`.`).
*   `-a <age_in_days>`: Files older than this many days will be considered 'stale temporal fragments'. Defaults to `30` days.
*   `-c <action>`: The action to perform. Can be `list` (default) or `delete`.
    *   `list`: Shows what would be cleaned without actually removing anything.
    *   `delete`: Actually removes the identified old files and empty directories.
*   `-h`: Display the usage help message.

### Examples:

1.  **List all digital dust bunnies in the current directory older than 30 days (default behavior):**
    ```bash
    ./src/dust_bunny_sweeper.sh
    ```

2.  **List stale temporal fragments in `/var/log` older than 90 days:**
    ```bash
    ./src/dust_bunny_sweeper.sh -d /var/log -a 90 -c list
    ```

3.  **Sweep away digital dust bunnies in `~/Downloads` older than 7 days:**
    ```bash
    ./src/dust_bunny_sweeper.sh -d ~/Downloads -a 7 -c delete
    ```

4.  **List empty directories in `/tmp`:**
    ```bash
    ./src/dust_bunny_sweeper.sh -d /tmp -a 0 -c list # Age 0 means all files are 'old', but primarily for empty dirs
    ```

## How it Works
The script uses the `find` command to locate files based on their modification time (`-mtime`) and to identify empty directories (`-empty -type d`). Depending on the chosen action, it will either print the paths of these items or attempt to remove them using `rm -f` for files and `rmdir` for empty directories.

## Safety Note
When using the `delete` action, ensure you understand what will be removed. It is highly recommended to run with `-c list` first to review the findings before proceeding with deletion. The script attempts to remove files and *empty* directories only. Directories that are not empty will not be removed by `rmdir`.
