# Nightly Echo-Chamber Cleanup

## Overview

The `nightly-echo-chamber-cleanup` utility is designed to help you declutter your digital archives by identifying and optionally removing duplicate files within a specified directory structure. It's like having a meticulous librarian for your files, ensuring no redundant echoes take up precious space.

It works by first grouping files by size, then by content hash (SHA256) to accurately pinpoint identical files. You can run it in a dry-run mode to see what would be removed, or in a full cleanup mode to actually delete the redundant copies.

## Usage

```bash
python src/cleanup.py --directory /path/to/your/files [--delete]
```

### Arguments:

*   `--directory <path>`: The root directory to scan for duplicate files. This argument is required.
*   `--delete`: (Optional) If provided, the utility will proceed to delete all but one instance of each identified duplicate group. **Use with caution!** Without this flag, it performs a dry-run and only reports the duplicates.

## Examples

### Dry Run (Recommended First Step)

To see which files are duplicates without deleting anything:

```bash
python src/cleanup.py --directory ~/my_documents
```

### Full Cleanup

To delete duplicate files (will prompt for confirmation):

```bash
python src/cleanup.py --directory ~/my_documents --delete
```

## How it Works

1.  **Directory Traversal**: Recursively walks through the specified directory.
2.  **Size Grouping**: Files are initially grouped by their size. This is a quick way to filter out many non-duplicates.
3.  **Content Hashing**: For files with identical sizes, their SHA256 hash is computed. Files with the same hash are considered duplicates.
4.  **Reporting/Deletion**: In dry-run mode, a report of duplicates and potential space savings is printed. In delete mode, all but one instance of each duplicate group are removed after user confirmation.

## Installation

This utility is self-contained and requires Python 3.6+.

```bash
# No special installation steps. Just run the script directly.
cd utils/nightly-echo-chamber-cleanup
python src/cleanup.py --help
```
