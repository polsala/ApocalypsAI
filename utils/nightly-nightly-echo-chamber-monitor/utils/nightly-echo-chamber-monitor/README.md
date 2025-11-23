# Nightly Echo Chamber Monitor

## Overview

The Nightly Echo Chamber Monitor is a whimsical yet practical utility designed to detect and report duplicate files within a specified directory. In the vast, ever-expanding digital landscape, redundant files can accumulate, consuming valuable space and making project management more complex. This tool helps you identify these 'echoes' of data, allowing you to clean up your repository and maintain a lean, efficient structure.

It works by calculating cryptographic hashes of file contents and grouping files that share the same hash, indicating they are exact duplicates.

## Usage

To run the monitor, simply execute the `monitor.py` script with the target directory as an argument:

```bash
python3 src/monitor.py --path /path/to/your/project
```

### Arguments

*   `--path <directory>`: The root directory to scan for duplicate files. This argument is required.
*   `--exclude <pattern>`: (Optional) A comma-separated list of glob-like patterns to exclude files or directories. E.g., `*.log,temp_dir/*,node_modules/`.

## Example Output

```
Scanning directory: /path/to/your/project

Found 2 groups of duplicate files:

--- Group 1 ---
Hash: 5f4dcc3b5aa765d61d8327deb882cf99
  - /path/to/your/project/docs/intro.md
  - /path/to/your/project/old_docs/introduction.md

--- Group 2 ---
Hash: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6
  - /path/to/your/project/assets/image.png
  - /path/to/your/project/backup/assets/image.png

Scan complete. Consider cleaning up these echoes.
```

## Development

This utility is written in Python 3.11 and is self-contained. Tests are located in the `tests/` directory and can be run using `python3 -m unittest`.
