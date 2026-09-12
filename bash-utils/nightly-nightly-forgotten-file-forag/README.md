# Nightly Forgotten File Forager

A whimsical Bash utility to forage for forgotten files older than a specified duration and suggest actions, helping you tidy up your digital wasteland.

## Summary

The `nightly-forgotten-file-forager` is your personal digital archaeologist, designed to unearth files that have been gathering digital dust. It scans specified directories for files that haven't been modified in a long time, presenting them as "forgotten relics." You can choose to simply list these relics or move them to a designated "digital archive" for later review, preventing them from cluttering your active workspaces.

## Usage

To use the Forager, simply run the `forage.sh` script with the desired options.

```bash
./src/forage.sh [-d <directory>] [-a <days>] [-m <archive_directory>] [-h]
```

### Options:

*   `-d <directory>`: The starting directory for foraging. The script will recursively search within this directory. Defaults to the current directory (`.`).
*   `-a <days>`: The age threshold in days. Files modified *more than* this many days ago will be considered "forgotten." Defaults to `90` days.
*   `-m <archive_directory>`: If provided, forgotten files will be moved to this directory. If the directory does not exist, the Forager will attempt to create it. If this option is omitted, the script will only list the forgotten files.
*   `-h`: Display the help message and exit.

### Examples:

1.  **List all forgotten files in the current directory (older than 90 days):**
    ```bash
    ./src/forage.sh
    ```

2.  **List forgotten files in `/home/user/documents` older than 180 days:**
    ```bash
    ./src/forage.sh -d /home/user/documents -a 180
    ```

3.  **Move forgotten files in `/var/log/old` older than 365 days to `/mnt/archive/logs`:**
    ```bash
    ./src/forage.sh -d /var/log/old -a 365 -m /mnt/archive/logs
    ```

4.  **List forgotten files in a specific project directory, older than 60 days:**
    ```bash
    ./src/forage.sh -d ~/projects/my-old-project -a 60
    ```

## How it Works

The `forage.sh` script leverages the powerful `find` command to locate files based on their modification time (`-mtime`). It then either prints the paths of these files to standard output or uses the `mv` command to relocate them to your specified archive directory. It's a simple yet effective way to manage digital entropy.

## Automated Tests

The utility includes a self-contained test script (`tests/test_forage.sh`) that creates a temporary file system, populates it with files of various ages, and then runs the `forage.sh` script against this controlled environment. This ensures the utility behaves as expected for both listing and moving operations, without affecting your actual files.

To run the tests:

```bash
./tests/test_forage.sh
```
