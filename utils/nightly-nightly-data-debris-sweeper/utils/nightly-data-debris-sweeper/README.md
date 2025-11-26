# Nightly Data Debris Sweeper

## Overview

The Nightly Data Debris Sweeper is a vigilant utility designed to help maintain a clean and efficient repository by identifying and reporting on "digital debris." In the post-apocalyptic digital landscape, every byte counts, and this tool helps you reclaim your precious disk space and keep your project organized.

It currently focuses on two key types of debris:
1.  **Stale Files**: Files that haven't been modified in a specified number of days, indicating potential obsolescence.
2.  **Empty Directories**: Directories that contain no files or subdirectories, often left behind after refactoring or deletions.

## Usage

Run the `sweeper.py` script from the command line.

```bash
python src/sweeper.py --path <repository_root_path> [--stale-days <number_of_days>]
```

### Arguments

*   `--path <repository_root_path>`: **Required**. The root directory to scan for debris.
*   `--stale-days <number_of_days>`: **Optional**. The number of days after which a file is considered "stale." Defaults to `90` days if not specified.

### Example

```bash
python src/sweeper.py --path . --stale-days 180
```

This command will scan the current directory and its subdirectories, reporting files not modified in the last 180 days and any empty directories found.

## Output

The utility prints its findings to standard output, categorizing them into "Stale Files" and "Empty Directories." If no debris is found, it will report a clean scan.

```
Scanning for digital debris in: /path/to/your/repo

--- Stale Files (not modified in 90 days) ---
- /path/to/your/repo/old_script.py (Last modified: 2023-01-15)
- /path/to/your/repo/docs/outdated_info.md (Last modified: 2022-11-01)

--- Empty Directories ---
- /path/to/your/repo/temp_folder/
- /path/to/your/repo/empty_logs/

Scan complete. Total stale files: 2, Total empty directories: 2.
```
