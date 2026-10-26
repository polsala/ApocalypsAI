# Nightly Digital Dust Bunny Sweeper

## Summary
The `nightly-digital-dust-bunny-sweeper` is a whimsical utility designed to help you identify and clear out old, forgotten files and directories on your system. It humorously refers to these stale digital artifacts as "digital dust bunnies," making system cleanup a slightly more entertaining chore in the post-apocalyptic landscape.

## Usage

### Prerequisites
- A Bash-compatible shell (e.g., Bash, Zsh)
- `find` utility (standard on most Unix-like systems)
- `xargs` utility (standard on most Unix-like systems)

### Running the Sweeper

1.  **Make the script executable:**
    ```bash
    chmod +x src/dust_bunny_sweeper.sh
    ```

2.  **Run with default settings:**
    By default, it scans the current directory (`.`) for files and directories older than 90 days.
    ```bash
    ./src/dust_bunny_sweeper.sh
    ```

3.  **Specify a target directory:**
    ```bash
    ./src/dust_bunny_sweeper.sh -d /path/to/your/wasteland/data
    ```

4.  **Specify a custom age (in days):**
    This example finds "dust bunnies" older than 30 days.
    ```bash
    ./src/dust_bunny_sweeper.sh -a 30
    ```

5.  **Combine options:**
    Scan `/var/log/old-archives` for items older than 180 days.
    ```bash
    ./src/dust_bunny_sweeper.sh -d /var/log/old-archives -a 180
    ```

6.  **Display help:**
    ```bash
    ./src/dust_bunny_sweeper.sh -h
    ```

### Output Example

```
Scanning '/path/to/your/wasteland/data' for digital dust bunnies older than 90 days...
---------------------------------------------------------------------
Behold! The following digital dust bunnies have been unearthed:
  - /path/to/your/wasteland/data/ancient_logs.tar.gz
  - /path/to/your/wasteland/data/forgotten_project
  - /path/to/your/wasteland/data/temp_backup.zip

Consider sweeping them away with a command like: rm -rf <path/to/dust_bunny>
Or for all listed: find '/path/to/your/wasteland/data' -maxdepth 1 -mtime +"90" -delete
```

## How it Works

The script uses the `find` command to locate files and directories within the specified `TARGET_DIR` that have a modification time (`-mtime`) older than the given `AGE_DAYS`. It specifically uses `find ... -maxdepth 1` to only look at immediate children of the target directory, preventing it from recursively diving into subdirectories and potentially overwhelming the user with too much information or accidentally suggesting deletion of important nested files. It then presents these findings in a user-friendly format, suggesting commands for their removal.

## Development & Testing

The `tests/test_dust_bunny_sweeper.sh` script provides automated, deterministic tests. It creates a temporary directory, populates it with files and directories with controlled modification timestamps (using `touch -t`), and then runs the main script against these controlled environments to verify its behavior.
