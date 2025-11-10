# Cosmic Dust Bunny Sweeper

## Overview

The `cosmic-dust-bunny-sweeper` is a whimsical yet practical utility designed to help you maintain a clean and efficient digital environment. It identifies and optionally removes 'cosmic dust bunnies' – old, forgotten files and empty directories that accumulate over time, cluttering your storage and potentially slowing down your system.

Think of it as a digital broom for your file system, ensuring your data is lean, mean, and ready for any apocalyptic scenario.

## Features

*   **Identify Old Files**: Scans a specified directory for files older than a given age threshold.
*   **Find Empty Directories**: Locates directories that contain no files or subdirectories.
*   **Dry Run Mode**: Preview what would be cleaned without making any changes.
*   **Configurable Age**: Set how old a file needs to be to be considered a 'dust bunny'.
*   **Detailed Report**: Provides a summary of found and (optionally) removed items.

## Installation

This utility is self-contained and written in Python 3.11+. No special installation steps are required beyond ensuring you have a compatible Python interpreter.

## Usage

To run the sweeper, navigate to the `src` directory and execute the `sweeper.py` script.

```bash
python3 utils/cosmic-dust-bunny-sweeper/src/sweeper.py --path /path/to/clean --age-days 30
```

### Arguments:

*   `--path <directory>` (required): The root directory to scan for dust bunnies.
*   `--age-days <int>` (optional, default: 30): Files older than this many days will be considered for removal.
*   `--dry-run` (optional): If present, the utility will only report what *would* be removed, without deleting anything.
*   `--verbose` (optional): Print detailed information about each file/directory found.

### Examples:

*   **List dust bunnies older than 60 days in your downloads folder (dry run):**
    ```bash
    python3 utils/cosmic-dust-bunny-sweeper/src/sweeper.py --path ~/Downloads --age-days 60 --dry-run
    ```
*   **Clean up empty directories and files older than 7 days in a temporary folder:**
    ```bash
    python3 utils/cosmic-dust-bunny-sweeper/src/sweeper.py --path /tmp/my_project_temps --age-days 7
    ```

## Development & Testing

Tests are located in `tests/test_sweeper.py` and can be run using `pytest` or `python -m unittest`.

```bash
python3 -m unittest utils/cosmic-dust-bunny-sweeper/tests/test_sweeper.py
```

All tests are deterministic and offline, using mocks to simulate file system interactions and time.
