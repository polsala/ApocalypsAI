# Digital Dust Bunny Sweeper

## 🧹 Overview

The Digital Dust Bunny Sweeper is a whimsical-yet-useful Python utility designed to help you reclaim precious disk space by identifying and optionally deleting old, unused files – your digital "dust bunnies." It's perfect for tidying up download folders, temporary directories, or any other digital nooks and crannies that tend to accumulate forgotten data.

## ✨ Features

*   **Recursive Scanning**: Scans specified directories and their subdirectories.
*   **Age-Based Filtering**: Identifies files older than a configurable number of days.
*   **Dry Run Mode**: Safely preview which files *would* be deleted without actually removing them.
*   **Deletion Confirmation**: Requires explicit `--delete` flag to perform actual deletions.

## 🚀 Usage

1.  **Navigate** to the utility's directory:
    ```bash
    cd utils/digital-dust-bunny-sweeper/src
    ```

2.  **Perform a dry run** (highly recommended!) to see which files would be affected. This will only print files, not delete them:
    ```bash
    python sweeper.py --path /path/to/your/messy/folder --age 90
    ```
    (This example will list files in `/path/to/your/messy/folder` that haven't been modified in the last 90 days.)

3.  **To actually delete** the identified files, add the `--delete` flag:
    ```bash
    python sweeper.py --path /path/to/your/messy/folder --age 180 --delete
    ```
    **⚠️ WARNING**: Use the `--delete` flag with caution! Always perform a dry run first to ensure you don't accidentally delete important files.

### Arguments:

*   `--path <directory>` (required): The root directory to scan for old files.
*   `--age <days>` (optional, default: 90): The minimum age in days for a file to be considered "old."
*   `--delete` (optional): Flag to enable actual file deletion. If omitted, only a dry run is performed.
