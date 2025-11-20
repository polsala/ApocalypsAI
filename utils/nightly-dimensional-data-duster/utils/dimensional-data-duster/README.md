# Dimensional Data Duster

## Overview

The Dimensional Data Duster is a whimsical yet powerful utility designed to help you clean up your digital dimensions by identifying and managing duplicate files across your specified directories. It uses content hashing to ensure true duplicates are found, not just files with the same name.

## Features

*   **Duplicate Detection**: Scans one or more directories for files with identical content.
*   **Content Hashing**: Uses SHA256 hashing for reliable duplicate identification.
*   **Dry Run Mode**: Preview which files would be affected before making any changes.
*   **Deletion Capability**: Safely remove duplicate files, keeping one original.

## Installation

This utility is self-contained and requires Python 3.8+.

```bash
# No special installation needed. Just run the script directly.
cd utils/dimensional-data-duster/src
python duster.py --help
```

## Usage

```bash
python duster.py <directory1> [directory2 ...] [--dry-run] [--delete]
```

### Arguments

*   `<directory1> [directory2 ...]`: One or more paths to directories to scan for duplicate files.
*   `--dry-run`: (Optional) Perform a scan and report duplicates without deleting any files. This is the default behavior if `--delete` is not specified.
*   `--delete`: (Optional) Delete duplicate files, keeping one instance of each unique file. **Use with caution!** This option overrides `--dry-run`.

### Examples

Scan your 'documents' and 'downloads' folders for duplicates (dry run):

```bash
python duster.py ~/documents ~/downloads
```

Scan your 'backups' folder and delete duplicates, keeping one copy:

```bash
python duster.py /mnt/backups --delete
```
