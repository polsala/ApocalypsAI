# Nightly Cosmic Dust Collector

## Overview

The Nightly Cosmic Dust Collector is a whimsical yet practical utility designed to help maintain a tidy repository or project directory. It scans a specified path for 'cosmic dust' – files that are both small in size and haven't been modified recently. These files often represent forgotten temporary files, old logs, or empty placeholders that can clutter a workspace.

By identifying and listing these files, the utility provides an easy way to review potential candidates for cleanup, archiving, or deletion, helping to keep your digital garden pristine.

## Usage

```bash
python src/collector.py <path_to_scan> [--max-size-kb <size_in_kb>] [--min-age-days <days_old>]
```

### Arguments:

*   `<path_to_scan>`: The root directory to begin scanning for dust.
*   `--max-size-kb <size_in_kb>`: (Optional) Maximum file size in kilobytes to consider as 'dust'. Defaults to 10 KB.
*   `--min-age-days <days_old>`: (Optional) Minimum age in days for a file to be considered 'dust'. Defaults to 30 days.

### Example:

To find files smaller than 5KB and older than 60 days in the current directory:

```bash
python src/collector.py . --max-size-kb 5 --min-age-days 60
```

## Output

The utility prints a list of identified 'dust' files to standard output, along with their size and last modification date. If no dust is found, it will indicate that the path is sparkling clean.

## Development

This utility is written in Python 3.11 and is self-contained. It uses standard library modules only.

## Tests

To run the tests, ensure you have `pytest` installed (`pip install pytest`):

```bash
python -m pytest tests/test_collector.py
```
