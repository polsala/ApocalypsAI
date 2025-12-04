# Nightly Data Scavenger & De-Duplicator

## Overview

In the digital wasteland, every byte of storage is precious. The ApocalypsAI Nightly Data Scavenger & De-Duplicator is a vital utility designed to reclaim lost space by identifying and eliminating redundant files. It meticulously scans specified directories, calculates cryptographic hashes of file contents, and reports or removes exact duplicates, ensuring your data reserves are lean and efficient.

Think of it as a digital archaeologist, sifting through the ruins of your file system to unearth and discard the unnecessary echoes of information.

## Features

*   **Content-Based Duplication Detection**: Uses SHA256 hashing to ensure files are truly identical, not just by name or size.
*   **Recursive Directory Scanning**: Explores subdirectories to find duplicates hidden deep within your file structure.
*   **Dry Run Mode (Default)**: Safely preview which files would be removed without making any actual changes.
*   **Live Removal Mode**: Execute the removal of duplicate files, keeping one original copy.
*   **Verbose Output**: Get detailed reports on identified duplicates and actions taken.

## Usage

The utility is a Python 3.11 script.

```bash
python src/deduplicator.py <directory1> [directory2 ...] [--remove] [--verbose]
```

### Arguments

*   `<directory1> [directory2 ...]`: One or more paths to directories that the scavenger should scan for duplicate files.
*   `--remove`: **(Optional)** If specified, the utility will actually delete the duplicate files, keeping only the first encountered instance of each unique file content. **Use with caution!**
*   `--verbose`: **(Optional)** Provides more detailed output, listing each duplicate set and the files that would be/were removed.

### Examples

1.  **Perform a dry run to see duplicates in a single directory:**
    ```bash
    python src/deduplicator.py /path/to/my/data
    ```

2.  **Perform a dry run with verbose output across multiple directories:**
    ```bash
    python src/deduplicator.py /path/to/archive /path/to/downloads --verbose
    ```

3.  **Actually remove duplicates in a directory (use with extreme care!):**
    ```bash
    python src/deduplicator.py /path/to/my/temp_files --remove
    ```

4.  **Remove duplicates with verbose output:**
    ```bash
    python src/deduplicator.py /path/to/my/temp_files --remove --verbose
    ```

## How it Works

1.  For each file encountered in the specified directories, the utility calculates its SHA256 hash.
2.  It stores these hashes along with the corresponding file paths.
3.  After scanning, it identifies all hashes that are associated with more than one file path. These are the duplicate sets.
4.  In dry run mode, it reports these findings.
5.  In live removal mode (`--remove`), for each duplicate set, it keeps the first file path encountered and deletes all subsequent files with the same hash.

## Development & Testing

To run the tests, navigate to the utility's root directory and execute:

```bash
python -m unittest tests/test_deduplicator.py
```

The tests use `unittest.mock` to simulate file system operations, ensuring determinism and isolation from the actual file system.
