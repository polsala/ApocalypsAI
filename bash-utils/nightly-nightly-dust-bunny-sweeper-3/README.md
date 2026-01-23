# Nightly Digital Dust Bunny Sweeper

A whimsical Bash utility to help you keep your digital space tidy by finding and optionally sweeping away old, forgotten files and empty directories – your very own 'digital dust bunnies'.

## Features

*   **Targeted Scanning**: Scan default temporary directories (`/tmp`, `/var/tmp`, `~/.cache`, `~/.local/share/Trash/files`) or specify your own paths.
*   **Age-Based Filtering**: Identify files older than a configurable number of days.
*   **Empty Directory Detection**: Automatically find and remove empty directories.
*   **Dry Run Mode**: See what would be swept away before any deletion occurs (default behavior).
*   **Confirmation Prompt**: Prevent accidental deletions with an interactive confirmation.
*   **Force Mode**: Bypass confirmation for automated cleanup tasks.
*   **Keep Empty Dirs**: Option to only remove old files, leaving empty directories intact.

## Installation

This is a standalone Bash script. No special installation is required beyond having Bash available on your system (which is standard on most Linux/macOS environments).

1.  Save the script to a file, e.g., `nightly-dust-bunny-sweeper.sh`.
2.  Make it executable:
    ```bash
    chmod +x nightly-dust-bunny-sweeper.sh
    ```
3.  (Optional) Move it to a directory in your `PATH` for easy access:
    ```bash
    sudo mv nightly-dust-bunny-sweeper.sh /usr/local/bin/
    ```

## Usage

```bash
nightly-dust-bunny-sweeper.sh [OPTIONS]
```

### Options:

*   `-p <path>`: Specify a directory to scan. Can be used multiple times to scan several custom paths. If no `-p` is given, it defaults to `/tmp`, `/var/tmp`, `~/.cache`, and `~/.local/share/Trash/files` (if they exist).
*   `-a <days>`: Files and directories older than `<days>` will be considered dust bunnies. Default: `7` days.
*   `-c`: Enable cleanup mode. This will delete the identified dust bunnies. Requires confirmation unless `-f` is also used.
*   `-f`: Force cleanup mode. Implies `-c` and bypasses the confirmation prompt. Use with caution!
*   `-k`: Keep empty directories. When in cleanup mode, only old files will be removed, and empty directories will be left untouched. Default: remove empty directories.
*   `-h`: Display the help message and exit.

### Examples:

*   **Dry run (default paths, default age of 7 days):**
    ```bash
    ./nightly-dust-bunny-sweeper.sh
    ```

*   **Dry run, scan `/var/log` for files older than 30 days:**
    ```bash
    ./nightly-dust-bunny-sweeper.sh -p /var/log -a 30
    ```

*   **Cleanup `/tmp` and `~/Downloads` for files older than 14 days, with confirmation:**
    ```bash
    ./nightly-dust-bunny-sweeper.sh -c -p /tmp -p ~/Downloads -a 14
    ```

*   **Force cleanup `/var/tmp` for files older than 2 days (no confirmation):**
    ```bash
    ./nightly-dust-bunny-sweeper.sh -f -p /var/tmp -a 2
    ```

*   **Cleanup files in default paths, but keep any empty directories:**
    ```bash
    ./nightly-dust-bunny-sweeper.sh -c -k
    ```

## How it Works

The script uses the `find` command to locate files and directories based on their modification time (`-mtime`) and type (`-type`). For cleanup, it uses `rm -rf`. It's designed to be safe by defaulting to a dry run and requiring confirmation for actual deletions, unless explicitly forced.

## Contributing

Feel free to suggest improvements or report issues! This utility is part of the ApocalypsAI project, aiming to provide useful and whimsical tools for the community.
