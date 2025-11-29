# Nightly Cosmic Dust Collector

## Overview

The Nightly Cosmic Dust Collector is a whimsical utility designed to help keep your project directories tidy by identifying "cosmic dust" – small, potentially forgotten, or empty files that accumulate over time. Think of it as a digital broom for your repository, sweeping up the tiny bits that don't quite belong.

It scans a specified directory, looking for files that fall below a configurable size threshold (defaulting to 1KB) or are completely empty. It then reports these files, allowing you to review and decide their fate.

## Features

*   **Scans for small files**: Identifies files smaller than a specified byte threshold.
*   **Detects empty files**: Specifically flags files with 0 bytes.
*   **Excludes common VCS directories**: Ignores `.git`, `.svn`, `.hg`, and `__pycache__` to prevent scanning version control internals or temporary build artifacts.
*   **Configurable threshold**: Adjust the maximum size for "dust" files.
*   **Simple reporting**: Outputs a list of identified files and their sizes.

## Usage

```bash
python src/dust_collector.py <directory_path> [--threshold <bytes>]
```

### Arguments:

*   `<directory_path>`: The path to the directory you want to scan for cosmic dust.
*   `--threshold <bytes>`: (Optional) The maximum file size in bytes to consider as "dust". Files smaller than or equal to this value will be reported. Defaults to `1024` bytes (1KB).

### Example:

```bash
# Scan the current directory for files <= 512 bytes
python src/dust_collector.py . --threshold 512

# Scan a specific project directory for files <= 1KB (default)
python src/dust_collector.py /path/to/my/project
```

## Output

The utility will print a list of files identified as cosmic dust, along with their sizes.

```
Scanning /path/to/my/project for cosmic dust (threshold: 1024 bytes)...

Cosmic Dust Found:
- /path/to/my/project/temp/log.txt (0 bytes)
- /path/to/my/project/old_script.sh (256 bytes)
- /path/to/my/project/data/empty.csv (0 bytes)

Total cosmic dust files found: 3
```

## Development

### Running Tests

To run the tests, navigate to the `nightly-cosmic-dust-collector` directory and execute:

```bash
python -m unittest tests/test_dust_collector.py
```
