# Nightly Forgotten File Finder

## 🕵️‍♂️ Unearthing the Digital Dust Bunnies 🕵️‍♀️

The Nightly Forgotten File Finder is a whimsical yet practical utility designed to help you reclaim precious disk space and maintain a tidy digital workspace. It scans specified directories for files that haven't been touched in a while, identifying those "forgotten" relics that might be silently accumulating digital dust.

Whether you want to simply report these old files or move them to a designated "quarantine" zone for later review, the Forgotten File Finder ensures your project directories remain lean and mean.

## ✨ Features

*   **Age-based Scanning**: Identify files older than a specified number of days (based on modification time).
*   **Report-Only Mode**: Get a list of forgotten files without taking any action.
*   **Quarantine Functionality**: Automatically move identified files to a separate "quarantine" directory for review or eventual deletion.
*   **Recursive Scanning**: Traverses subdirectories to find forgotten files deep within your project.
*   **Self-Contained**: Written in Python 3.11, with no external dependencies beyond the standard library.

## 🚀 Usage

```bash
python src/finder.py --path <directory_to_scan> --age <days> [--quarantine <quarantine_directory>] [--report-only]
```

### Arguments:

*   `--path <directory_to_scan>` (required): The root directory to start scanning for forgotten files.
*   `--age <days>` (required): The minimum age in days for a file to be considered "forgotten" (based on modification time).
*   `--quarantine <quarantine_directory>` (optional): If provided, forgotten files will be moved to this directory. If the directory doesn't exist, it will be created.
*   `--report-only` (optional): If set, the utility will only report the forgotten files and will not move them, even if `--quarantine` is specified.

### Examples:

1.  **Report all files in `/tmp/my_project` older than 30 days:**
    ```bash
    python src/finder.py --path /tmp/my_project --age 30 --report-only
    ```

2.  **Move files older than 90 days from `/home/user/downloads` to `/home/user/quarantine_zone`:**
    ```bash
    python src/finder.py --path /home/user/downloads --age 90 --quarantine /home/user/quarantine_zone
    ```

3.  **Scan current directory for files older than 7 days and move them to a local `_quarantine` folder:**
    ```bash
    python src/finder.py --path . --age 7 --quarantine ./_quarantine
    ```

## 🛠️ Development

To run tests:

```bash
python -m unittest tests/test_finder.py
```
