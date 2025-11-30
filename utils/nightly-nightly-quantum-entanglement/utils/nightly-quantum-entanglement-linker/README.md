# Nightly Quantum Entanglement Linker

The Nightly Quantum Entanglement Linker is a whimsical-yet-powerful utility designed to bring order to your digital cosmos by identifying and optionally consolidating duplicate files through the magic of hard links. Just as quantum entanglement links particles across vast distances, this linker connects identical files on your filesystem, saving precious disk space and reducing data redundancy.

## ✨ Features

*   **Duplicate Detection**: Scans a specified directory for files with identical content using SHA256 hashing.
*   **Space Saving**: Optionally replaces duplicate files with hard links to a single original, freeing up disk space without altering file paths or accessibility.
*   **Safe Operations**: Includes a "dry-run" mode to preview changes before execution.
*   **Whimsical Naming**: Because even apocalypse preparation needs a touch of charm.

## 🚀 Usage

This utility is a Python 3.11 script.

### Prerequisites

*   Python 3.11 or higher.
*   No external dependencies beyond standard library modules (`os`, `hashlib`, `sys`, `collections`, `argparse`).

### Running the Utility

Navigate to the `src` directory within the utility folder and run `linker.py` with the desired arguments.

```bash
python src/linker.py <directory_to_scan> [--mode <operation_mode>]
```

#### Arguments:

*   `<directory_to_scan>`: The root directory where the utility will begin its scan for duplicate files. This is a required positional argument.

#### Options:

*   `--mode <operation_mode>`: Specifies how the utility should operate. Choose one of the following:
    *   `report` (Default): Lists all groups of duplicate files found, showing their SHA256 hash and the paths to each duplicate. No changes are made to the filesystem.
    *   `link-dry-run`: Performs a "dry run" of the linking process. It will report which files *would* be replaced by hard links, but no actual modifications are made. This is highly recommended for previewing changes.
    *   `link-execute`: **DANGER!** This mode will actually replace duplicate files with hard links. For each group of duplicates, it will keep the first file encountered as the "original" and replace all other duplicates in that group with hard links pointing to the original. **Use with caution and ensure you have backups.**

### Examples:

1.  **Report all duplicate files in your `documents` folder:**
    ```bash
    python src/linker.py /home/user/documents --mode report
    ```

2.  **See what files would be hard-linked in your `backups` directory (dry run):**
    ```bash
    python src/linker.py /mnt/backups --mode link-dry-run
    ```

3.  **Execute hard-linking in your `downloads` folder (use with extreme care!):**
    ```bash
    python src/linker.py /home/user/downloads --mode link-execute
    ```

## 🧪 Testing

The utility includes a comprehensive test suite using Python's `unittest` framework. All tests are deterministic and offline, using mocks to simulate filesystem operations without actual disk I/O.

To run the tests, navigate to the utility's root directory and execute:

```bash
python -m unittest tests/test_linker.py
```

## ⚠️ Important Considerations

*   **Hard Links**: Hard links are a Unix-like filesystem feature. They are not separate copies; they are additional directory entries that point to the same underlying data on disk. Deleting one hard link does not delete the data until all hard links to that data are removed.
*   **Filesystem Support**: Hard links are typically supported on filesystems like ext4, XFS, NTFS (on Windows, with some limitations). They usually cannot span across different filesystems or partitions.
*   **Data Integrity**: While hard linking is generally safe, always back up critical data before running `link-execute` mode.
*   **Symbolic Links**: The utility explicitly skips symbolic links to prevent unintended behavior or infinite loops.
