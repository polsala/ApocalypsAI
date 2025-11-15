# Digital Dust Bunny Sweeper

## Overview

The ApocalypsAI Nightly Integrator presents the `digital-dust-bunny-sweeper`! In the vast digital cosmos, even the most pristine systems can accumulate 'digital dust bunnies' – those forgotten, unused files and empty directories that silently consume precious disk space and clutter your digital landscape.

This whimsical utility is designed to help you identify and, if you choose, sweep away these digital remnants, ensuring your directories remain as clean and efficient as possible for the coming (or ongoing) apocalypse.

## Features

*   **Empty Directory Detection**: Finds and reports directories that contain no files or subdirectories.
*   **Old Log File Identification**: Locates `.log` files older than a specified number of days (default: 30 days).
*   **Temporary File Spotting**: Identifies files ending with `.tmp` or starting with `tmp_`.
*   **Interactive Cleanup**: Offers an option to delete the identified dust bunnies after review.

## Usage

```bash
python src/sweeper.py <path_to_scan> [--days <int>] [--delete]
```

*   `<path_to_scan>`: The root directory to begin the sweep.
*   `--days <int>`: (Optional) Number of days after which log files are considered 'old'. Default is 30.
*   `--delete`: (Optional) If present, the utility will prompt for confirmation before deleting identified dust bunnies. Without this flag, it will only report.

### Examples

Scan your home directory for dust bunnies, reporting only:

```bash
python src/sweeper.py ~/ --days 60
```

Scan a project directory and interactively delete identified items:

```bash
python src/sweeper.py ./my_project --delete
```

## Installation

This utility is self-contained and requires Python 3.11+. No external dependencies are needed beyond the standard library.

1.  Navigate to the `utils/digital-dust-bunny-sweeper/` directory.
2.  Run the script directly.

## Development & Testing

To run the tests, navigate to the utility's root directory and execute:

```bash
python -m unittest tests/test_sweeper.py
```
