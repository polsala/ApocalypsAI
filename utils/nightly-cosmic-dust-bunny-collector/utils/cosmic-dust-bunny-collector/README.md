# Cosmic Dust Bunny Collector

## Whimsical Purpose
In the grand scheme of the ApocalypsAI repository, even the most meticulously organized digital spaces can accumulate 'cosmic dust bunnies' – those old, forgotten files that linger like echoes of past computations. This utility is designed to help you sweep them away, ensuring your directories remain pristine and ready for whatever the future (or lack thereof) holds.

## What it Does
The Cosmic Dust Bunny Collector identifies and optionally removes files from a specified directory that are older than a given age threshold and, optionally, match specific file patterns. It supports a dry-run mode to preview deletions before committing.

## How to Use

### Prerequisites
*   Python 3.6+ (standard library only)

### Installation
This utility is self-contained. Simply navigate to its directory.

### Running the Collector
```bash
python src/collector.py <directory> --age <days> [--patterns <pattern1> <pattern2> ...] [--delete]
```

#### Arguments:
*   `<directory>`: The path to the directory you want to clean.
*   `--age <days>`: Files older than this many days will be considered 'dust bunnies'.
*   `--patterns <pattern1> <pattern2> ...`: (Optional) One or more glob-style patterns (e.g., `*.log`, `temp_*`) to filter files. If not provided, all files older than the age threshold are considered.
*   `--delete`: (Optional) If present, files will actually be deleted. **Use with caution!** By default, the utility runs in dry-run mode and only prints what *would* be deleted.

### Examples

#### Dry run: Find all files older than 30 days in `/tmp/my_data`
```bash
python src/collector.py /tmp/my_data --age 30
```

#### Dry run: Find all `.log` and `.tmp` files older than 7 days in `/var/logs`
```bash
python src/collector.py /var/logs --age 7 --patterns "*.log" "*.tmp"
```

#### Delete: Remove all files older than 90 days in `/old_backups`
```bash
python src/collector.py /old_backups --age 90 --delete
```
