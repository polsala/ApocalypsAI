# Nightly Digital Dust Sweeper

## Overview
The `nightly-digital-dust-sweeper` is a whimsical yet practical utility designed to help you maintain a clean and efficient file system. It scans a specified directory for two common forms of "digital dust bunnies": empty directories and broken symbolic links. By identifying and optionally removing these, it helps declutter your storage and prevent potential issues.

## Features
- **Empty Directory Detection**: Scans for and lists all empty directories within a given path.
- **Broken Symlink Detection**: Identifies and lists symbolic links that point to non-existent targets.
- **Optional Cleanup**: Provides a `--clean` flag to automatically remove detected empty directories and broken symlinks.
- **Dry Run by Default**: By default, the utility only reports findings without making any changes.

## Installation
This utility is self-contained and written in Python 3.11+. No external dependencies are required beyond the standard library.

## Usage
```bash
python3 src/dust_sweeper.py --path /path/to/scan
```

### Arguments
- `--path <directory>`: **Required**. The root directory to start scanning from.
- `--clean`: **Optional**. If provided, the utility will proceed to remove detected empty directories and broken symbolic links. Use with caution!
- `--verbose`: **Optional**. If provided, prints more detailed information during the scan.

### Examples
1. **Scan and report (dry run):**
   ```bash
   python3 src/dust_sweeper.py --path ~/my_project_folder
   ```

2. **Scan and clean:**
   ```bash
   python3 src/dust_sweeper.py --path /var/log/old_logs --clean
   ```

3. **Scan and report with verbose output:**
   ```bash
   python3 src/dust_sweeper.py --path /tmp --verbose
   ```

## How it Works
The utility uses Python's `os` and `pathlib` modules to traverse the file system.
- For empty directories, it checks if `os.listdir()` returns an empty list for a given directory.
- For broken symlinks, it checks if `os.path.islink()` is true and `os.path.exists()` is false for a given path.

## Contributing
Feel free to suggest improvements or report issues!
