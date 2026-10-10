# Nightly Resource Scavenger

## Overview

The `nightly-resource-scavenger` is a whimsical yet practical Bash utility designed to help you keep your system tidy by identifying and 'reclaiming' old, unused files. Think of it as a digital scavenger hunt, where the goal is to find forgotten 'relics' (files) that are past their prime and 'recycle' them for the collective good (free up disk space).

It operates in two modes: a safe dry-run mode (default) to show you what it *would* scavenge, and an actual scavenging mode that performs the deletions.

## Features

*   **Age-based Scavenging**: Targets files older than a specified number of days.
*   **Directory Targeting**: Scans one or more specified directories.
*   **Dry Run Mode**: Safely preview which files would be affected without making any changes.
*   **Actual Scavenge Mode**: Deletes the identified old files.
*   **Whimsical Reporting**: Provides a summary of 'relics identified' and 'reclaimed'.

## Usage

```bash
./src/main.sh [-d <days>] [-r] <directory1> [directory2 ...]
```

### Arguments:

*   `-d <days>`: Specifies the age threshold in days. Files older than this many days will be considered for scavenging. Defaults to `7` days if not specified.
*   `-r`: Activates the 'actual scavenging' mode. **Use with caution!** Without this flag, the script runs in dry-run mode, only reporting what it *would* do.
*   `<directory1> [directory2 ...]`: One or more paths to the directories you want the scavenger to inspect.

### Examples:

1.  **Dry run to see files older than 30 days in `/var/log` and `/tmp`:**
    ```bash
    ./src/main.sh -d 30 /var/log /tmp
    ```

2.  **Actually scavenge files older than 7 days in `/home/user/downloads`:**
    ```bash
    ./src/main.sh -r /home/user/downloads
    ```

3.  **Scavenge files older than 14 days in multiple locations:**
    ```bash
    ./src/main.sh -d 14 -r /opt/app/logs /var/cache/apt/archives
    ```

## Installation

This is a standalone Bash script. Simply ensure it's executable:

```bash
chmod +x src/main.sh
```

Then you can run it as shown in the Usage section.

## Contributing

Feel free to suggest improvements or new features! The ApocalypsAI community thrives on collective ingenuity.
