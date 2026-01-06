# Nightly Relic Hunter

## Summary
The `nightly-relic-hunter` is a whimsical-yet-useful bash utility designed to help you discover and manage "digital dust bunnies" or "forgotten files" on your filesystem. It hunts down files and directories that haven't been modified in a specified period, presenting them as "digital relics" that might be candidates for archival or deletion.

## Usage
```bash
./src/relic_hunter.sh <path> [days_old]
```

### Arguments
*   `<path>`: The starting directory where the relic hunt will begin. The script will traverse up to 5 levels deep from this path.
*   `[days_old]`: (Optional) The age threshold in days. Files and directories modified *more than* this many days ago will be considered digital relics. If not provided, the default threshold is 90 days.

### Examples
*   To find all relics older than 90 days in your home directory:
    ```bash
    ./src/relic_hunter.sh ~/ 90
    ```
*   To find all relics older than 180 days in `/var/log`:
    ```bash
    ./src/relic_hunter.sh /var/log 180
    ```
*   To use the default 90-day threshold for your Downloads folder:
    ```bash
    ./src/relic_hunter.sh ~/Downloads
    ```

## How it Works
The script uses the `find` command to efficiently locate files and directories based on their last modification time (`-mtime`). It then uses `stat` and `date` to calculate and display their exact age and last modification timestamp in a human-readable format.

**Important Safety Note:** This utility is purely a reporting tool. It **does not** delete, move, or modify any files or directories. It only lists potential digital relics, allowing you to review them and decide on appropriate action.

## Dependencies
This script relies on standard GNU core utilities: `bash`, `find`, `stat`, and `date`. It is designed for Linux environments where these GNU versions are typically available. Some options (e.g., `stat -c %Y`, `date -d`) might behave differently on BSD/macOS systems.
