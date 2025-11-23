# Nightly Digital Debris Sweeper

## Overview

The Nightly Digital Debris Sweeper is a vigilant utility designed to keep your filesystem pristine by identifying and optionally removing broken symbolic links and empty directories. In the post-apocalyptic digital landscape, clutter can lead to confusion and inefficiency. This sweeper ensures your paths are clear and your storage is optimized.

## Features

*   **Broken Symlink Detection**: Scans for symbolic links that point to non-existent files or directories.
*   **Empty Directory Identification**: Locates directories that contain no files or subdirectories.
*   **Safe Listing Mode**: Preview the "debris" before any removal actions are taken.
*   **Removal Capability**: Safely remove identified broken symlinks and empty directories.

## Usage

```bash
python src/sweeper.py --path <directory_to_scan> [--remove-symlinks] [--remove-empty-dirs] [--verbose]
```

### Arguments

*   `--path <directory>`: The root directory to start scanning from. **Required.**
*   `--remove-symlinks`: If specified, broken symbolic links will be removed. Otherwise, they will only be listed.
*   `--remove-empty-dirs`: If specified, empty directories will be removed. Otherwise, they will only be listed.
*   `--verbose`: Print detailed information about scanned items and actions.

## Examples

1.  **List all broken symlinks and empty directories in the current directory (and subdirectories):**
    ```bash
    python src/sweeper.py --path .
    ```

2.  **Remove broken symlinks in `/data/projects`:**
    ```bash
    python src/sweeper.py --path /data/projects --remove-symlinks
    ```

3.  **Remove empty directories in `/tmp/builds` and show verbose output:**
    ```bash
    python src/sweeper.py --path /tmp/builds --remove-empty-dirs --verbose
    ```

4.  **Clean up both broken symlinks and empty directories in `/home/user/downloads`:**
    ```bash
    python src/sweeper.py --path /home/user/downloads --remove-symlinks --remove-empty-dirs
    ```
