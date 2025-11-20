# Dimensional Data Duster

## Overview
The Dimensional Data Duster is your trusty companion in the never-ending battle against digital clutter. In a world where every byte counts, this utility helps you identify and report on duplicate files across your specified directories, allowing you to reclaim valuable disk space. It's like a digital broom, sweeping away the echoes of redundant data!

## Features
- Scans one or more directories for files.
- Identifies duplicates based on SHA256 content hash.
- Reports duplicate groups, showing all paths to identical files.
- Dry-run mode to preview duplicates without deletion.

## Usage

```bash
python src/duster.py <directory1> [directory2 ...] [--dry-run]
```

**Example:**
```bash
python src/duster.py /home/user/documents /mnt/backup --dry-run
```

This will scan `/home/user/documents` and `/mnt/backup` for duplicate files and print a report without deleting anything.

## How it Works
The duster first groups files by size. For files with identical sizes, it then calculates a SHA256 hash of their content. If two files have the same size AND the same hash, they are considered duplicates. This two-step process optimizes performance by avoiding hashing large numbers of unique files.

## Installation
This utility is self-contained and requires Python 3.8+ (or compatible). No external dependencies are needed beyond the standard library.

```bash
# Navigate to the utility's directory
cd utils/dimensional-data-duster/
# Run it directly
python src/duster.py /path/to/scan
```
