# Nightly Data Dust Bunny Duster

## Overview

In the post-apocalyptic digital landscape, even the most resilient data can accumulate digital "dust bunnies" – empty directories and zero-byte files that clutter the filesystem and consume precious mental bandwidth. The **Nightly Data Dust Bunny Duster** is a whimsical-yet-essential utility designed to sweep away these digital detritus, ensuring your data repositories remain pristine and efficient.

It scans a specified directory, identifies empty folders and files with no content, and can either report them or, with your explicit permission, remove them. Keep your digital bunkers tidy!

## Usage

```bash
python src/duster.py <path_to_scan> [--delete]
```

- `<path_to_scan>`: The root directory from which to start dusting.
- `--delete`: (Optional) If provided, the utility will actually delete the identified empty directories and zero-byte files. Without this flag, it will only report them.

### Examples

**Just report what needs dusting:**
```bash
python src/duster.py /path/to/your/data
```

**Clean up the dust bunnies:**
```bash
python src/duster.py /path/to/your/data --delete
```

## Features

- Identifies empty directories.
- Identifies zero-byte files.
- Dry-run mode (default) to preview changes.
- Deletion mode for actual cleanup.
- Recursive scanning from a specified root.

## Installation

This utility is self-contained and requires only Python 3.6+ (or compatible). No external dependencies are needed beyond the standard library.

```bash
# Navigate to the utility's directory
cd utils/nightly-data-dust-bunny-duster
# Run it directly
python src/duster.py . --delete
```
