# Quantum Quake Deduplicator

## Overview

The `Quantum Quake Deduplicator` is a vital tool for any survivor navigating the digital ruins. It meticulously scans a specified directory, identifying files with identical content (duplicates) using cryptographic hashing. Once identified, it can either report these redundant files or, with your explicit permission, purge them from existence, freeing up precious storage space.

Think of it as a digital scavenger, sifting through the rubble of your filesystem to reclaim lost bytes.

## Features

*   **Content-Based Duplication**: Identifies duplicates by comparing file hashes (SHA256 by default), ensuring true content identity, not just name or size.
*   **Recursive Scanning**: Traverses subdirectories to find duplicates across your entire data hoard.
*   **Dry Run Mode**: Safely preview which files would be deleted without making any changes.
*   **Interactive Deletion**: Prompts for confirmation before deleting any files, giving you ultimate control.
*   **Lightweight & Self-Contained**: Written in Python, with no external dependencies beyond the standard library.

## Usage

```bash
python src/deduplicator.py <directory_path> [--dry-run] [--delete]
```

### Arguments:

*   `<directory_path>`: The path to the directory you want to scan for duplicates.

### Options:

*   `--dry-run`: Perform a scan and report duplicates, but do not delete any files. This is the default behavior if `--delete` is not specified.
*   `--delete`: After identifying duplicates, prompt the user to confirm deletion of all but one instance of each duplicate set. **Use with caution!**

## Examples

### 1. Scan for duplicates (dry run):

```bash
python src/deduplicator.py /path/to/your/data/hoard
```

### 2. Scan and interactively delete duplicates:

```bash
python src/deduplicator.py /path/to/your/data/hoard --delete
```

## Development

To run tests:

```bash
python -m unittest tests/test_deduplicator.py
```
