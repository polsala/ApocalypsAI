# Nightly Echo Chamber Purifier

## Overview

The Nightly Echo Chamber Purifier is a whimsical-yet-useful utility designed to help you declutter your digital spaces by identifying and managing duplicate files. Like a diligent cosmic janitor, it sweeps through your specified directories, detecting redundant data that might be echoing across your file system, consuming precious storage.

It works by calculating the cryptographic hash of each file's content. If two files have the same hash, they are considered identical.

## Features

*   **Duplicate Detection**: Scans one or more directories for files with identical content.
*   **Content-Based Hashing**: Uses SHA-256 hashing to ensure accurate duplicate identification, regardless of file name or modification date.
*   **Report Generation**: Outputs a clear list of duplicate files, grouped by their content.
*   **Safe Operation**: By default, it only reports duplicates; no files are deleted without explicit user action (though this version focuses on reporting).

## Installation

This utility is self-contained and written in Python 3.11+. No external dependencies are required beyond the standard library.

1.  Navigate to the `utils/nightly-echo-chamber-purifier/` directory.
2.  The `purifier.py` script is directly runnable.

## Usage

```bash
python src/purifier.py <directory1> [directory2 ...]
```

**Example:**

To find duplicates in your `documents` and `downloads` folders:

```bash
python src/purifier.py ~/documents ~/downloads
```

### Output

The script will print groups of duplicate files. Each group will start with the hash of the duplicate content, followed by the paths to all files sharing that content.

```
Duplicate Group (SHA256: a1b2c3d4e5f6...)
  - /path/to/file1.txt
  - /path/to/another/file1.txt
  - /path/to/backup/file1_copy.txt

Duplicate Group (SHA256: f6e5d4c3b2a1...)
  - /path/to/image.jpg
  - /path/to/gallery/image_copy.jpg
```

## Development & Testing

To run the tests:

```bash
python -m unittest tests/test_purifier.py
```
