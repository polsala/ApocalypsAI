# Nightly Echo Chamber Purifier

## Overview

The Nightly Echo Chamber Purifier is a whimsical yet highly practical utility designed to cleanse your digital spaces of redundant data. It scans specified directories for duplicate files by comparing their cryptographic hashes, helping you identify and optionally remove unnecessary copies that clutter your storage and obscure important information.

Think of it as a digital sound engineer, eliminating the echoes and reverberations of identical files so your data can resonate clearly.

## Features

*   **Duplicate Detection**: Efficiently identifies files with identical content using SHA256 hashing.
*   **Configurable Scan Paths**: Specify one or more directories to scan.
*   **Reporting Mode**: Lists all detected duplicate groups and their locations without making any changes.
*   **Deletion Mode**: Safely removes all but one instance of each duplicate file group, freeing up disk space.

## Usage

To run the purifier, navigate to the `utils/nightly-echo-chamber-purifier/src` directory and execute `purifier.py`.

```bash
# Scan a directory and report duplicates (default behavior)
python purifier.py --path /path/to/your/directory

# Scan multiple directories
python purifier.py --path /path/to/dir1 --path /path/to/dir2

# Scan and delete all but one copy of each duplicate group
python purifier.py --path /path/to/your/directory --delete-duplicates

# Get help
python purifier.py --help
```

## Installation

This utility is self-contained and requires no special installation beyond a standard Python 3.x environment. Just ensure you have Python installed.

## Development & Testing

To run the tests, navigate to the `utils/nightly-echo-chamber-purifier/tests` directory and execute `pytest` (if installed) or `python -m unittest test_purifier.py`.

```bash
cd utils/nightly-echo-chamber-purifier/tests
python -m unittest test_purifier.py
```
