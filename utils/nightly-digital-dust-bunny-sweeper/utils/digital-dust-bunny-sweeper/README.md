# Digital Dust Bunny Sweeper

## Overview

The ApocalypsAI Nightly Integrator proudly presents the **Digital Dust Bunny Sweeper**! In the grand tradition of preparing for... well, anything, it's crucial to keep our digital spaces tidy. This utility helps you identify and report those pesky, forgotten files – the 'digital dust bunnies' – that accumulate over time, hogging precious disk space.

Think of it as a friendly robot vacuum for your file system, but instead of sucking up lint, it points out files that are old, large, or both, so you can decide their fate.

## Features

*   **Directory Scanning**: Recursively scans a specified directory.
*   **Age-Based Detection**: Identifies files older than a configurable number of days.
*   **Size-Based Detection**: Flags files larger than a configurable minimum size.
*   **Whimsical Reporting**: Presents findings with a touch of ApocalypsAI charm.

## Usage

```bash
python src/sweeper.py --path /path/to/scan [--age-days <int>] [--min-size-mb <int>]
```

### Arguments:

*   `--path <directory>`: The root directory to start scanning from. (Required)
*   `--age-days <int>`: Files older than this many days will be flagged. Default: 30 days.
*   `--min-size-mb <int>`: Files larger than this many megabytes will be flagged. Default: 10 MB.

### Examples:

Scan your downloads folder for files older than 60 days or larger than 50MB:

```bash
python src/sweeper.py --path ~/Downloads --age-days 60 --min-size-mb 50
```

Scan your entire home directory for any file older than a year (365 days) regardless of size:

```bash
python src/sweeper.py --path ~ --age-days 365 --min-size-mb 0
```

## Installation

This utility is self-contained and requires Python 3.6+.

1.  Navigate to the `utils/digital-dust-bunny-sweeper` directory.
2.  Run directly using `python src/sweeper.py`.

## Development & Testing

To run the tests, navigate to the utility's root directory and execute:

```bash
python -m unittest tests/test_sweeper.py
```
