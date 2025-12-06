# Echo Chamber Resonator

## Purpose

The "Echo Chamber Resonator" is a whimsical-yet-useful utility designed to detect and report duplicate files within a specified directory structure. It achieves this by calculating cryptographic hashes (SHA256) for each file and grouping together any files that share identical content. This helps in identifying redundant assets, cleaning up repositories, and ensuring data consistency.

## Usage

To use the Echo Chamber Resonator, simply run the `resonator.py` script with the path to the directory you wish to scan:

```bash
python src/resonator.py /path/to/your/directory
```

### Example Output

```
Scanning /path/to/your/directory...

Found 2 groups of duplicate files:

--- Group 1 ---
Hash: a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6e7f8a9b0c1d2e3f4a5b6c7d8e9f0a1b2
  - /path/to/your/directory/documents/report_v1.txt
  - /path/to/your/directory/archive/old_report.txt

--- Group 2 ---
Hash: f0e9d8c7b6a5f4e3d2c1b0a9f8e7d6c5b4a3f2e1d0c9b8a7f6e5d4c3b2a1f0e9
  - /path/to/your/directory/images/logo.png
  - /path/to/your/directory/assets/backup_logo.png
```

## Installation

This utility is self-contained and requires no external dependencies beyond Python 3.6+.

```bash
cd utils/echo-chamber-resonator
python src/resonator.py .
```
