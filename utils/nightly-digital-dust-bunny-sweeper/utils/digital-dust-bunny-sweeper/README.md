# Digital Dust Bunny Sweeper

## Overview

Welcome, digital janitor! The `digital-dust-bunny-sweeper` is a whimsical yet practical utility designed to help you declutter your digital spaces. It scans specified directories for 'digital dust bunnies' – files that are either very old, seemingly unused, or exact duplicates – and reports them, allowing you to decide whether to sweep them away.

Think of it as a friendly robot vacuum for your filesystem, identifying the forgotten corners and redundant clutter that accumulate over time.

## Features

*   **Age-based Detection**: Finds files older than a specified threshold (default: 365 days).
*   **Duplicate Detection**: Identifies exact duplicate files based on their content hash.
*   **Clear Reporting**: Presents findings in an easy-to-read format, categorizing files as 'fluffy dust bunnies' (old files) or 'tangled dust clumps' (duplicates).

## Installation

This utility is self-contained and written in Python 3.11+. No special installation steps are required beyond having a compatible Python interpreter.

## Usage

To run the sweeper, navigate to the `utils/digital-dust-bunny-sweeper/src` directory and execute `dust_bunny_sweeper.py`.

```bash
python3 dust_bunny_sweeper.py <directory_to_scan> [--age-days <days>] [--min-size <bytes>]
```

### Arguments:

*   `<directory_to_scan>`: The path to the directory you want to scan for dust bunnies. (Required)
*   `--age-days <days>`: (Optional) Files older than this many days will be flagged as 'fluffy dust bunnies'. Default is 365 days.
*   `--min-size <bytes>`: (Optional) Only consider files larger than this size (in bytes) for scanning. Useful for ignoring tiny log files or configuration snippets. Default is 0.

### Example:

Scan your `~/Downloads` folder for files older than 90 days:

```bash
python3 dust_bunny_sweeper.py ~/Downloads --age-days 90
```

Scan your `~/Documents` folder for duplicates and old files, ignoring anything smaller than 1KB:

```bash
python3 dust_bunny_sweeper.py ~/Documents --min-size 1024
```

## Output

The utility will print a summary of its findings, listing old files and groups of duplicate files, along with their sizes and paths. It will not delete any files; it only reports them.

## Contributing

Feel free to suggest improvements or new 'dust bunny' detection methods! Pull requests are welcome.
