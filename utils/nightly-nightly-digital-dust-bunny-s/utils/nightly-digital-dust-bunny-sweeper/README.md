# Nightly Digital Dust Bunny Sweeper

## Overview

The `nightly-digital-dust-bunny-sweeper` is a whimsical yet practical utility designed to keep your project directories pristine. It identifies and, optionally, removes common digital 'dust bunnies': empty directories and broken symbolic links. Regular use helps maintain a clean, efficient, and clutter-free repository, making navigation and development smoother.

## Features

*   **Empty Directory Detection**: Scans a specified path for directories that contain no files or subdirectories.
*   **Broken Symbolic Link Detection**: Identifies symbolic links that point to non-existent files or directories.
*   **Dry Run Mode**: Preview what would be swept without making any changes.

## Usage

To run the sweeper, navigate to the utility's directory or call it directly:

```bash
# From the repository root:
python utils/nightly-digital-dust-bunny-sweeper/src/sweeper.py <path_to_scan> [--dry-run]

# Example: Scan the current directory in dry-run mode
python utils/nightly-digital-dust-bunny-sweeper/src/sweeper.py . --dry-run

# Example: Sweep (delete) empty directories and broken symlinks in 'my_project_dir'
python utils/nightly-digital-dust-bunny-sweeper/src/sweeper.py my_project_dir
```

### Arguments

*   `<path_to_scan>`: The root directory from which to start scanning. Required.
*   `--dry-run`: If present, the utility will only report what *would* be swept, without making any changes to the file system. Recommended for initial runs.

## Development

### Running Tests

To ensure the sweeper is working as expected, run its self-contained tests:

```bash
# From the utility's root directory:
python -m unittest tests/test_sweeper.py
```

## Contributing

Feel free to suggest enhancements or report issues. The goal is to keep our digital spaces clean and efficient!
