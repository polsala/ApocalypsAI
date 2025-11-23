# Nightly Cosmic Dust Bunny Collector

## Overview

The 'Cosmic Dust Bunny Collector' is a whimsical-yet-useful utility designed to help maintain a tidy digital environment. It scans specified directories for common digital 'dust bunnies' – temporary files, hidden system files, empty folders, and old log files – and provides options to clean them up. Think of it as a tiny, automated janitor for your file system, ensuring your digital space remains pristine for the next apocalyptic event.

## Features

*   **Identifies Common Clutter**: Targets `.DS_Store`, `thumbs.db`, `__pycache__`, `.tmp` files, and empty directories.
*   **Aged Log File Cleanup**: Can remove `.log` files older than a specified number of days.
*   **Dry Run Mode**: Safely preview what would be deleted without making any changes.
*   **Configurable Paths**: Specify one or more directories to scan.

## Usage

```bash
python src/collector.py --help

# Scan current directory and subdirectories, report findings (dry run by default)
python src/collector.py .

# Scan multiple directories
python src/collector.py /path/to/project1 /path/to/downloads

# Scan and actually delete the identified dust bunnies
python src/collector.py --clean /path/to/scan

# Scan and delete log files older than 30 days
python src/collector.py --clean --log-age 30 /path/to/logs

# Scan and delete, but exclude specific patterns (e.g., keep .git folders)
# (Note: Current version does not support explicit excludes, but future versions might!)
```

## Installation

This utility is self-contained. Simply navigate to its directory and run the `collector.py` script with Python 3.11+.

```bash
cd utils/nightly-cosmic-dust-bunny-collector
python src/collector.py --help
```

## Development

### Running Tests

```bash
python -m unittest tests/test_collector.py
```

## License

This project is licensed under the MIT License - see the `LICENSE` file in the repository root for details.
