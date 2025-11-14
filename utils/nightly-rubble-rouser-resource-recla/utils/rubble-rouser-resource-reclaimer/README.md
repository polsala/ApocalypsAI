# Rubble-Rouser Resource Reclaimer

## Overview
In the desolate digital wastes of the post-apocalypse, every byte counts. The `Rubble-Rouser Resource Reclaimer` is your trusty companion for sifting through the digital debris, identifying redundant data, and reclaiming precious disk space. Whether it's duplicate manifest files, forgotten log archives, or empty bunkers (directories), this utility helps you tidy up your filesystem.

## Features
-   **Duplicate File Detection**: Scans for files with identical content (using MD5 hashes) and groups them.
-   **Empty Directory Identification**: Locates and lists directories that contain no files or subdirectories.
-   **Ancient Artifact Discovery**: Finds files older than a specified number of days, perfect for purging forgotten archives.
-   **Safe Operation**: By default, it only lists findings. Use the `--delete` flag with caution to remove identified items.

## Usage

```bash
python3 src/reclaimer.py --help
```

```
usage: reclaimer.py [-h] [--path PATH] [--duplicates] [--empty-dirs] [--old-files DAYS_OLD] [--delete]

A whimsical-yet-useful Python utility to reclaim disk space.

options:
  -h, --help            show this help message and exit
  --path PATH           The root directory to scan (default: current directory).
  --duplicates          Find and list duplicate files.
  --empty-dirs          Find and list empty directories.
  --old-files DAYS_OLD  Find and list files older than DAYS_OLD days.
  --delete              WARNING: Actually delete the identified files/directories. Use with extreme caution.
```

### Examples

1.  **Find all duplicate files in the current directory:**
    ```bash
    python3 src/reclaimer.py --duplicates
    ```

2.  **List empty directories in a specific path:**
    ```bash
    python3 src/reclaimer.py --path /var/log/old_archives --empty-dirs
    ```

3.  **Identify files older than 365 days in your home directory (without deleting):**
    ```bash
    python3 src/reclaimer.py --path ~/ --old-files 365
    ```

4.  **DANGER: Delete all duplicate files and empty directories in a test folder:**
    ```bash
    python3 src/reclaimer.py --path ./test_cleanup --duplicates --empty-dirs --delete
    ```

## Installation

No special installation required. Just ensure you have Python 3.6+ installed. The utility is self-contained.

## Contributing

Contributions are welcome! Feel free to raise issues or submit pull requests for new features or bug fixes. Remember, every byte saved is a victory against digital entropy!
