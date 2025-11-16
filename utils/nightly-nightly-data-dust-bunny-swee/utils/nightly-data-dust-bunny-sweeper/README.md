# Nightly Data Dust Bunny Sweeper

## Overview

The 'Nightly Data Dust Bunny Sweeper' is a utility designed to help you maintain a tidy digital environment by identifying and optionally removing common forms of digital clutter: duplicate files, empty directories, and files that haven't been touched in ages.

Think of it as a diligent, tiny robot sweeping through your file system, making sure no digital dust bunnies accumulate and slow down your post-apocalyptic data retrieval.

## Features

*   **Duplicate File Detection**: Identifies files with identical content using cryptographic hashing.
*   **Empty Directory Detection**: Finds directories that contain no files or subdirectories.
*   **Ancient File Detection**: Locates files older than a specified number of days, perfect for clearing out forgotten archives.
*   **Safe Operation**: Offers a 'list only' mode to preview changes before committing to deletion.

## Usage

```bash
python src/sweeper.py --help
```

### Examples:

1.  **List all duplicate files in a directory (and its subdirectories):**
    ```bash
    python src/sweeper.py --path /path/to/scan --duplicates --list-only
    ```

2.  **Delete all empty directories in a specific path:**
    ```bash
    python src/sweeper.py --path /path/to/clean --empty-dirs --delete
    ```

3.  **Find files older than 365 days in your 'archives' folder:**
    ```bash
    python src/sweeper.py --path /path/to/archives --old-files 365 --list-only
    ```

4.  **Perform a full sweep (list duplicates, empty dirs, and files older than 180 days):**
    ```bash
    python src/sweeper.py --path /path/to/data --duplicates --empty-dirs --old-files 180 --list-only
    ```

## Installation

This utility is self-contained and requires Python 3.8+ (tested with 3.11). No external dependencies are needed beyond the standard library.

```bash
# Navigate to the utility's directory
cd utils/nightly-data-dust-bunny-sweeper

# Run directly
python src/sweeper.py --path . --duplicates --list-only
```

## Development & Testing

To run the tests for this utility:

```bash
# Navigate to the utility's directory
cd utils/nightly-data-dust-bunny-sweeper

# Run tests
python -m unittest tests/test_sweeper.py
```
