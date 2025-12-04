# Nightly Chrono-Shift File Renamer

## Overview

The `nightly-chrono-shift-file-renamer` is a utility designed to bring order to chaotic file directories. It renames files based on their creation or modification timestamps, applying a consistent `YYYYMMDD_HHMMSS` format. This helps in chronologically organizing files, especially useful for photos, documents, or logs that might have arbitrary names but accurate timestamps.

## Features

*   **Timestamp-based Renaming**: Uses either the file's creation time or last modification time.
*   **Consistent Format**: Renames files to `YYYYMMDD_HHMMSS_originalfilename.ext` or `YYYYMMDD_HHMMSS.ext`.
*   **Conflict Resolution**: Automatically appends a counter (e.g., `_01`, `_02`) for files with identical timestamps.
*   **Dry Run Mode**: Preview renaming actions without making any changes to the filesystem.
*   **Flexible Naming**: Option to retain a part of the original filename or just use the timestamp.

## Usage

```bash
python src/renamer.py <directory_path> [--use-creation-time] [--dry-run] [--keep-original-name]
```

### Arguments:

*   `<directory_path>`: The path to the directory containing the files to be renamed.

### Options:

*   `--use-creation-time`: Use the file's creation timestamp instead of the last modification timestamp. By default, modification time is used.
*   `--dry-run`: Perform a dry run. The utility will print the proposed renames without actually modifying any files.
*   `--keep-original-name`: When renaming, append a sanitized version of the original filename after the timestamp (e.g., `YYYYMMDD_HHMMSS_original.ext`). By default, files are renamed to just `YYYYMMDD_HHMMSS.ext`.

## Examples

1.  **Basic rename using modification time (default) and keeping original name, dry run:**
    ```bash
    python src/renamer.py ./my_scraps --keep-original-name --dry-run
    ```

2.  **Rename using creation time, without keeping original name, actual run:**
    ```bash
    python src/renamer.py ./old_logs --use-creation-time
    ```

3.  **Rename all files in current directory, dry run:**
    ```bash
    python src/renamer.py . --dry-run
    ```

## Installation

This utility is self-contained and requires Python 3.11+. No external dependencies are needed beyond the standard library.

To run:

1.  Navigate to the `utils/nightly-chrono-shift-file-renamer/` directory.
2.  Execute the `src/renamer.py` script with your desired arguments.
