# Cosmic Dust Bunny Sweeper

## Description

The 'Cosmic Dust Bunny Sweeper' is a delightful utility designed to help you maintain a pristine filesystem by identifying and optionally removing old files and empty directories. Think of those forgotten temporary files or empty folders as 'cosmic dust bunnies' that accumulate over time, cluttering your digital space. This tool helps you sweep them away with a touch of whimsy.

It's particularly useful for development environments, build directories, or any location where temporary artifacts tend to pile up.

## Features

*   **Age-based File Cleanup**: Identifies files older than a specified number of days.
*   **Empty Directory Cleanup**: Finds and lists/removes directories that contain no files or subdirectories.
*   **Dry Run Mode**: Preview what would be deleted without making any changes.
*   **Recursive Scanning**: Scans a specified root directory and all its subdirectories.

## Installation

This utility is self-contained and written in Python 3.11+. No external dependencies are required beyond the standard library.

1.  Navigate to the utility's directory:
    ```bash
    cd utils/cosmic-dust-bunny-sweeper
    ```
2.  You can run it directly using Python.

## Usage

Run the `sweeper.py` script with the desired arguments.

```bash
python src/sweeper.py --path <directory_to_clean> [--age <days>] [--dry-run]
```

### Arguments:

*   `--path <directory>`: **Required**. The root directory to start sweeping from.
*   `--age <days>`: Optional. Files older than this many days will be considered 'dust bunnies'. Defaults to `30` days.
*   `--dry-run`: Optional. If present, the utility will only list what *would* be deleted, without performing any actual deletions. Highly recommended for initial runs.

### Examples:

1.  **List all dust bunnies older than 60 days in the current directory (dry run):**
    ```bash
    python src/sweeper.py --path . --age 60 --dry-run
    ```

2.  **Actually sweep away dust bunnies older than 30 days in a specific build folder:**
    ```bash
    python src/sweeper.py --path /path/to/my/build/folder
    ```

3.  **Find and remove only empty directories in a project folder (by setting age to 0 and relying on empty dir detection):**
    ```bash
    python src/sweeper.py --path /path/to/my/project --age 0
    ```

## Testing

To run the tests, navigate to the utility's directory and execute the test script:

```bash
cd utils/cosmic-dust-bunny-sweeper
python -m unittest tests/test_sweeper.py
```
