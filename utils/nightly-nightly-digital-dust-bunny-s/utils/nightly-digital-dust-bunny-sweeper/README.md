# Digital Dust Bunny Sweeper

## Overview

The Digital Dust Bunny Sweeper is a utility designed to help you maintain a tidy file system by identifying and optionally removing empty directories and old, specified temporary files. Think of it as a digital vacuum cleaner, tidying up the forgotten corners of your storage.

It's particularly useful in development environments, download folders, or any directory that accumulates temporary files and empty folders over time.

## Features

*   **Empty Directory Detection**: Scans a specified path for any subdirectories that contain no files or further subdirectories.
*   **Old Temporary File Cleanup**: Identifies files with common temporary extensions (e.g., `.tmp`, `.log`, `.bak`) that are older than a configurable number of days.
*   **Dry Run Mode**: Preview what would be deleted without actually making any changes.
*   **Configurable Age and Extensions**: Customize how 'old' a file needs to be and which file extensions to target.

## Usage

```bash
python3 src/sweeper.py --path /path/to/scan [--age DAYS] [--extensions .ext1 .ext2] [--dry-run]
```

### Arguments:

*   `--path <directory>`: **Required**. The root directory to start scanning from.
*   `--age <days>`: Optional. The minimum age in days for a temporary file to be considered 'old'. Defaults to `30` days.
*   `--extensions <.ext1 .ext2 ...>`: Optional. A space-separated list of file extensions to consider as temporary. Defaults to `.tmp .log .bak .old .swp`.
*   `--dry-run`: Optional. If present, the utility will only report what *would* be deleted without performing any actual deletions.

### Examples:

Scan your downloads folder for empty directories and `.tmp` files older than 60 days, showing what would be deleted:

```bash
python3 src/sweeper.py --path ~/Downloads --age 60 --extensions .tmp --dry-run
```

Clean up empty directories and default temporary files older than 30 days in your project directory:

```bash
python3 src/sweeper.py --path ~/my_project
```

## Installation

This utility is self-contained and requires Python 3.6+ (tested with 3.11). No external dependencies are needed.

1.  Navigate to the `utils/nightly-digital-dust-bunny-sweeper` directory.
2.  Run the `src/sweeper.py` script directly.

## Contributing

Feel free to suggest improvements or report issues via the main repository's issue tracker.
