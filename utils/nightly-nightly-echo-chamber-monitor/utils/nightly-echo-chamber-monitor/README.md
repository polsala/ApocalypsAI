# Nightly Echo Chamber Monitor

## Purpose
In the post-apocalyptic digital landscape, redundant data can clog precious storage and obscure vital information. The **Nightly Echo Chamber Monitor** is a whimsical yet practical utility designed to detect and report duplicate files within a specified directory. By identifying these 'echoes,' it helps maintain a lean, efficient, and well-organized repository.

## How it Works
This utility recursively scans a given directory, calculates a SHA256 hash for each file, and then groups files that share the same hash. It reports all groups of files where more than one file has an identical hash, indicating a duplicate.

## Usage

```bash
python src/monitor.py <directory_to_scan>
```

### Example

```bash
# Scan the current directory for duplicates
python src/monitor.py .

# Scan a specific 'archives' folder
python src/monitor.py /path/to/your/archives
```

### Output Example

```
Scanning '/path/to/your/repo' for duplicate files...

Found 2 groups of duplicate files:

Group 1 (SHA256: a1b2c3d4e5f6...):
  - /path/to/your/repo/docs/old_report.txt
  - /path/to/your/repo/archives/report_copy.txt

Group 2 (SHA256: f6e5d4c3b2a1...):
  - /path/to/your/repo/images/logo.png
  - /path/to/your/repo/assets/backup_logo.png
```

## Installation
No special installation is required beyond a standard Python 3.11+ environment. The utility is self-contained.
