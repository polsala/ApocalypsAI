# Nightly Data Dust Bunny Duster

## Whimsical Purpose
In the chaotic aftermath, digital detritus accumulates faster than you can say 'nuclear winter'. The Data Dust Bunny Duster is here to help you reclaim precious storage space by sniffing out those pesky duplicate files that are silently multiplying across your salvaged data drives. Think of it as a digital broom, sweeping away the redundant fluff so your essential survival data can breathe.

## Practical Usefulness
This utility scans one or more specified directories, calculates cryptographic hashes for all files, and reports any files that are exact duplicates. This is invaluable for:
- **Storage Optimization**: Free up disk space by identifying files that can be safely deleted (after verification).
- **Data Integrity**: Ensure you don't have conflicting versions of 'the last known recipe for irradiated squirrel stew'.
- **Cleanup Automation**: Integrate into your nightly routines to keep your data repository lean and efficient.

## How to Use

```bash
python src/duster.py <directory1> [directory2] ...
```

### Arguments:
- `<directory1> [directory2] ...`: One or more paths to directories that the duster should scan for duplicates. The utility will recursively traverse these directories.

### Example:
```bash
python src/duster.py /mnt/salvaged_data/documents /home/survivor/backups
```

## Output
The duster will print a report to standard output, grouping duplicate files together. Each group will show the hash and the paths to all identical files.

```
--- Duplicate Files Report ---

--- Duplicate Group ---
Hash: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2
  - /path/to/file1.txt
  - /path/to/another/file1.txt

--- Duplicate Group ---
Hash: x1y2z3a4b5c6d7e8f9g0h1i2j3k4l5m6n7o8p9q0r1s2t3u4v5w6x7y8z9a0b1c2
  - /path/to/image.jpg
  - /path/to/backup/image.jpg

--- End of Report ---
```

## Installation
No special installation is required beyond a Python 3.11+ environment. The utility is self-contained.

## Development
To run tests:
```bash
python -m unittest tests/test_duster.py
```
