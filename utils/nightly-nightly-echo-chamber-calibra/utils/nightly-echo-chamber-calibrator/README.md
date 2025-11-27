# Nightly Echo Chamber Calibrator

## Silence the Redundancy, Amplify the Efficiency!

The ApocalypsAI Nightly Integrator proudly presents the **Echo Chamber Calibrator** – your essential tool for decluttering digital spaces. In the post-apocalyptic landscape, every byte counts. This utility helps you identify and eliminate redundant files, ensuring your precious storage isn't filled with digital echoes.

Whether it's forgotten backups, accidental copies, or just plain digital clutter, the Calibrator will scan your specified directories, find identical files based on their content, and give you the power to remove the duplicates, keeping only one pristine original.

## Features

*   **Content-Based Detection**: Uses SHA256 hashing to accurately identify identical files, regardless of name or timestamp.
*   **Multi-Directory Scan**: Scan one or more directories for duplicates.
*   **Dry Run Mode**: Preview which files would be deleted before making any changes.
*   **Safe Deletion**: Optionally remove duplicates, always preserving the first encountered instance.

## Installation

This utility is self-contained and written in Python 3.11+. No external dependencies are required beyond the standard library.

## Usage

Run the `calibrator.py` script from the `src/` directory.

```bash
python3 utils/nightly-echo-chamber-calibrator/src/calibrator.py --help
```

### Basic Scan (Dry Run)

To find duplicates in `/path/to/my/data` and `/path/to/my/backups` without deleting anything:

```bash
bash
python3 utils/nightly-echo-chamber-calibrator/src/calibrator.py \
  --path /path/to/my/data \
  --path /path/to/my/backups
```

### Delete Duplicates (with confirmation)

To find and delete duplicates in `/path/to/my/data`, keeping only one copy of each file. **Use with caution!**

```bash
python3 utils/nightly-echo-chamber-calibrator/src/calibrator.py \
  --path /path/to/my/data \
  --delete
```

### Arguments

*   `--path <directory>`: (Required, can be specified multiple times) The directory to scan for duplicate files.
*   `--delete`: (Optional) If specified, duplicates will be deleted. By default, only a dry run report is generated.
*   `--block-size <bytes>`: (Optional) The block size in bytes to use when calculating file hashes. Defaults to 65536 (64KB).
