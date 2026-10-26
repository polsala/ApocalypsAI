# Nightly Digital Dust Bunny Sweeper

## Overview
In the vast, ever-expanding digital cosmos, forgotten files and empty directories accumulate like cosmic dust bunnies, silently consuming precious space and cluttering your system. The `nightly-dust-bunny-sweeper` is your whimsical-yet-powerful ally in the ongoing battle against digital entropy!

This Bash utility helps you identify and, optionally, sweep away those digital 'dust bunnies' – old, unused files (like temporary files, logs, backups) and lonely, empty directories – keeping your system spry and efficient.

## Features
*   **Whimsical Reporting**: Get a charming report of all identified digital fluff.
*   **Configurable Age**: Define how 'old' a file needs to be to qualify as a dust bunny.
*   **Dry Run Mode (Default)**: Safely preview what would be swept away without making any changes.
*   **Clean Mode**: Unleash the broom and actually delete the identified dust bunnies (use with caution!).
*   **Targeted Sweeping**: Specify a directory to scan, or let it tidy up your current location.

## Usage

### Prerequisites
*   A Bash-compatible shell (most Linux/macOS systems have this).
*   Standard utilities: `find`, `rm`, `rmdir`.

### Running the Sweeper

1.  **Make the script executable**:
    ```bash
    chmod +x src/dust_bunny_sweeper.sh
    ```

2.  **Basic Dry Run (default)**:
    To see what dust bunnies are lurking in your current directory, without deleting anything:
    ```bash
    ./src/dust_bunny_sweeper.sh
    ```

3.  **Scan a Specific Directory (Dry Run)**:
    To check for dust bunnies in `/var/log` that are older than 90 days:
    ```bash
    ./src/dust_bunny_sweeper.sh -d 90 /var/log
    ```

4.  **Clean Mode (USE WITH CAUTION!)**:
    To actually delete dust bunnies older than 180 days in your `~/Downloads` directory:
    ```bash
    ./src/dust_bunny_sweeper.sh -c -d 180 ~/Downloads
    ```
    **Always review the dry run output before using `-c`!**

5.  **Help Message**:
    ```bash
    ./src/dust_bunny_sweeper.sh -h
    ```

## Options
*   `-d <days>`: Files older than `<days>` will be considered dust bunnies (default: `90`).
*   `-c`: **Clean mode**. Actually delete found dust bunnies. **USE WITH EXTREME CAUTION!**
*   `-h`: Show the help message and exit.

## Examples

```bash
# Find old files and empty directories in the current path (dry run)
./src/dust_bunny_sweeper.sh

# Find files older than 365 days in /tmp (dry run)
./src/dust_bunny_sweeper.sh -d 365 /tmp

# Clean up old log files in /var/log (actual deletion)
./src/dust_bunny_sweeper.sh -c /var/log

# Clean up temporary files older than 30 days in your home directory
./src/dust_bunny_sweeper.sh -c -d 30 ~/
```

## Contributing
Feel free to contribute to making our digital spaces cleaner and more whimsical! Report issues, suggest features, or submit pull requests.
