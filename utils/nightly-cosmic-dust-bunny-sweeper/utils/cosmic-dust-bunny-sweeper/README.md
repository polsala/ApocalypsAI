# Cosmic Dust Bunny Sweeper

## Description

Welcome, digital voyager, to the Cosmic Dust Bunny Sweeper! In the vast expanse of your file system, digital detritus accumulates like cosmic dust bunnies, slowing down your operations and obscuring vital data. This whimsical-yet-useful utility is designed to help you identify and optionally purge these unwanted remnants: empty directories and files older than a specified age.

Keep your systems sparkling clean and optimized, ready for any interdimensional anomaly or impending... well, you know.

## Features

*   **Empty Directory Detection**: Scans a specified path for directories that contain no files or subdirectories.
*   **Aged File Identification**: Locates files older than a configurable number of days.
*   **Dry Run Mode**: Preview all potential deletions without making any changes.
*   **Interactive Deletion**: Confirm each deletion or all deletions before permanent removal.

## Usage

```bash
python src/sweeper.py <path_to_scan> [--dry-run] [--age-days <int>]
```

### Arguments:

*   `<path_to_scan>`: The root directory from which to begin the cosmic sweep. (Required)
*   `--dry-run`: If present, the utility will only report what *would* be deleted, without actually removing anything. (Optional)
*   `--age-days <int>`: Files older than this many days will be considered 'cosmic dust' and flagged for potential removal. Defaults to 30 days. (Optional)

### Examples:

Scan your 'downloads' folder for empty directories and files older than 60 days, in dry-run mode:

```bash
python src/sweeper.py ~/Downloads --dry-run --age-days 60
```

Perform a full sweep and delete empty directories and files older than 7 days in your 'temp' folder:

```bash
python src/sweeper.py /var/tmp --age-days 7
```

## Installation

This utility is self-contained and requires Python 3.6+ (tested with 3.11). No external dependencies are needed beyond the standard library.

Simply navigate to the `utils/cosmic-dust-bunny-sweeper/` directory and run the `sweeper.py` script.

## Testing

To run the tests, navigate to the utility's root directory and execute:

```bash
python -m unittest tests/test_sweeper.py
```
