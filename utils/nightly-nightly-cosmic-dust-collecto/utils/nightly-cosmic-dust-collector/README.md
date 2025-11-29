# Nightly Cosmic Dust Collector

## Overview

The Nightly Cosmic Dust Collector is a whimsical yet practical utility designed to help maintain a clean and organized repository. It scans specified directories for 'cosmic dust' – small, potentially forgotten, or empty files that might be cluttering your project.

By identifying these files, the collector helps you decide whether they are still needed, can be archived, or should be removed, contributing to a tidier and more efficient workspace.

## Usage

```bash
python src/dust_collector.py <path_to_scan> [--max-size-kb <size>] [--exclude <dir1> <dir2> ...]
```

- `<path_to_scan>`: The root directory to begin scanning.
- `--max-size-kb`: (Optional) The maximum file size in kilobytes to consider as 'dust'. Files larger than this will be ignored. Defaults to 1 KB.
- `--exclude`: (Optional) A space-separated list of directory names to exclude from the scan (e.g., `.git`, `node_modules`, `__pycache__`).

### Example

To scan the current directory for files smaller than 5KB, excluding `node_modules` and `.venv`:

```bash
python src/dust_collector.py . --max-size-kb 5 --exclude node_modules .venv
```

## Output

The utility will print a list of identified 'dust' files, their sizes, and their paths to the console.

```
Cosmic Dust Report for /path/to/scan (max size: 1 KB):
---------------------------------------------------

Found 3 pieces of cosmic dust:
- /path/to/scan/temp/log.txt (0.1 KB)
- /path/to/scan/empty.txt (0.0 KB)
- /path/to/scan/old_config.bak (0.5 KB)

---------------------------------------------------
Scan complete. Total dust collected: 3 files.
```

## Development

This utility is written in Python 3.11 and is self-contained. Tests are located in the `tests/` directory.

To run tests:

```bash
python -m unittest tests/test_dust_collector.py
```
