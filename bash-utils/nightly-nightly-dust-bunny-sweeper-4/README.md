# Nightly Digital Dust Bunny Sweeper

## Summary
In the vast, ever-expanding digital wasteland, forgotten files and empty directories accumulate like spectral dust bunnies, silently consuming precious storage and mental clarity. The `nightly-dust-bunny-sweeper` is your trusty broom, designed to identify and sweep away these digital detritus, restoring order and efficiency to your system.

## Features
*   **Ancient Data Fragment Detection**: Locates files older than a specified number of days.
*   **Echoing Void Identification**: Finds and lists empty directories.
*   **Report Mode**: Safely lists all identified 'dust bunnies' without making any changes.
*   **Sweep Protocol (Delete Mode)**: Aggressively removes identified old files and empty directories.

## Usage

### Prerequisites
*   Bash shell
*   `find`, `rm`, `rmdir` (standard Unix utilities)

### Running the Sweeper

```bash
./src/dust-bunny-sweeper.sh [-d <directory>] [-a <age_days>] [-c <action>]
```

**Options:**
*   `-d <directory>`: The root directory to scan for dust bunnies. Defaults to the current directory (`.`).
*   `-a <age_days>`: Files older than this many days will be considered 'ancient data fragments'. Defaults to `30` days.
*   `-c <action>`: Specifies the action to take.
    *   `report` (default): Lists all identified dust bunnies without deleting them.
    *   `delete`: Proceeds with the deletion of identified old files and empty directories. **Use with caution!**

### Examples

1.  **Report all digital dust bunnies in the current directory older than 60 days:**
    ```bash
    ./src/dust-bunny-sweeper.sh -a 60 -c report
    ```

2.  **Find and delete old log files (older than 7 days) and empty directories in `/var/log`:**
    ```bash
    sudo ./src/dust-bunny-sweeper.sh -d /var/log -a 7 -c delete
    ```

3.  **Just list empty directories in your home directory:**
    ```bash
    ./src/dust-bunny-sweeper.sh -d ~/ -a 9999 -c report # Use a very large age to focus on empty dirs
    ```

## Safety First!
Always run the script in `report` mode (`-c report`) first to review what will be affected before executing the `delete` action. The ApocalypsAI Nightly Integrator is not responsible for any data lost due to reckless digital dust bunny sweeping.
