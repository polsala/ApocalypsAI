# Resource Scavenger Optimizer

In the desolate wastes of your hard drive, every byte counts. The `resource-scavenger-optimizer` is your trusty companion for navigating the digital ruins, helping you scavenge for precious disk space by identifying large and duplicate files. Prepare your system for the inevitable digital winter by reclaiming valuable storage!

## Features

*   **Large File Detection**: Pinpoint files exceeding a specified size threshold.
*   **Duplicate File Identification**: Uncover redundant copies of files using robust hashing.
*   **Comprehensive Reporting**: Get a clear overview of your scavenging opportunities.

## Installation

This utility is self-contained and requires Python 3.8+.

```bash
# No installation needed, just run it!
cd utils/resource-scavenger-optimizer
python src/scavenger.py --help
```

## Usage

Run the scavenger from the utility's root directory:

```bash
python src/scavenger.py --path /path/to/scan --min-size 10 # Find files > 10MB
```

To find duplicates:

```bash
python src/scavenger.py --path /path/to/scan --duplicates
```

To do both:

```bash
python src/scavenger.py --path /path/to/scan --min-size 5 --duplicates
```

### Arguments

*   `--path <directory>`: The directory to scan (required).
*   `--min-size <MB>`: Minimum size in megabytes for a file to be considered 'large'. (Default: 10MB)
*   `--duplicates`: Flag to enable duplicate file detection.

## Example Output

```
--- Resource Scavenger Report ---
Scanning: /home/user/my_data

[LARGE FILES ( > 10.0 MB )]
  - /home/user/my_data/archives/old_backup.zip (15.2 MB)
  - /home/user/my_data/videos/epic_fail.mp4 (22.1 MB)

[DUPLICATE FILES]
  - Hash: a1b2c3d4e5f6g7h8i9j0k1l2m3n4o5p6
    - /home/user/my_data/docs/report_v1.pdf
    - /home/user/my_data/docs/report_final.pdf
  - Hash: q1w2e3r4t5y6u7i8o9p0a1s2d3f4g5h6
    - /home/user/my_data/images/cat.jpg
    - /home/user/my_data/temp/cat_copy.jpg

--- Scavenging complete! ---
```
